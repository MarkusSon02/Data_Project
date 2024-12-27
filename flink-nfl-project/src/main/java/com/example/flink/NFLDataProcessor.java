import org.apache.flink.api.common.functions.RichFlatMapFunction;
import org.apache.flink.api.java.tuple.Tuple2;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.table.api.*;
import org.apache.flink.table.api.bridge.java.StreamTableEnvironment;
import org.apache.flink.types.Row;
import org.apache.flink.util.Collector;

import java.util.ArrayList;
import java.util.List;

public class DynamicSchemaFlink {

    public static void main(String[] args) throws Exception {
        // Step 1: Set up Flink environment
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        StreamTableEnvironment tEnv = StreamTableEnvironment.create(env);

        // Path to CSV file
        String csvFilePath = "/path/to/csv";

        // Step 2: Extract first 5 rows
        DataStream<String> rawStream = env.readTextFile(csvFilePath);
        DataStream<String> firstFiveRows = rawStream.process(new ProcessFunction<String, String>() {
            private int count = 0;

            @Override
            public void processElement(String value, Context ctx, Collector<String> out) throws Exception {
                if (count < 5) {
                    out.collect(value);
                    count++;
                }
            }
        });

        // Step 3: Collect rows for schema inference
        List<Row> rows = new ArrayList<>();
        List<String[]> rowData = new ArrayList<>();
        firstFiveRows.flatMap(new RichFlatMapFunction<String, Tuple2<Integer, String>>() {
            @Override
            public void flatMap(String value, Collector<Tuple2<Integer, String>> out) {
                rowData.add(value.split(",")); // Split CSV by delimiter
            }
        }).executeAndCollect().forEachRemaining(tuple -> rows.add(Row.of((Object[]) tuple.f1.split(","))));

        // Step 4: Dynamically infer schema
        Schema.Builder schemaBuilder = Schema.newBuilder();
        for (int colIndex = 0; colIndex < rowData.get(0).length; colIndex++) {
            String columnName = "col" + colIndex;
            schemaBuilder.column(columnName, DataTypes.STRING()); // Assume STRING for simplicity
        }
        Schema schema = schemaBuilder.build();

        // Step 5: Use `fromValues` to create a Flink table
        Table initialTable = tEnv.fromValues(schema, rows);
        tEnv.createTemporaryView("InitialTable", initialTable);

        // Step 6: Query the table (for demonstration purposes)
        Table result = tEnv.sqlQuery("SELECT * FROM InitialTable");
        result.execute().print();
    }
}
