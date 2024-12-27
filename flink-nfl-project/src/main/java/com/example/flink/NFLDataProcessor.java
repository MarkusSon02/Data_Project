import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.table.api.EnvironmentSettings;
import org.apache.flink.table.api.Table;
import org.apache.flink.table.api.bridge.java.StreamTableEnvironment;

public class NFLDataProcessor {
    public static void main(String[] args) throws Exception {
        // Create Flink batch environment
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

        // Use batch mode for Table API
        EnvironmentSettings settings = EnvironmentSettings.newInstance().inBatchMode().build();
        StreamTableEnvironment tableEnv = StreamTableEnvironment.create(env, settings);

        // Register CSV source
        tableEnv.executeSql(
                "CREATE TABLE nfl_data (" +
                "  EPA DOUBLE, " +
                "  Season INT " +
                "  /* Add more fields from your dataset */ " +
                ") WITH (" +
                "  'connector' = 'filesystem', " +
                "  'path' = '/path/to/your/nfl_data.csv', " +
                "  'format' = 'csv'" +
                ")"
        );

        // Query the data
        Table result = tableEnv.sqlQuery(
                "SELECT Season, AVG(EPA) AS avg_epa " +
                "FROM nfl_data " +
                "GROUP BY Season"
        );

        // Output the result to a file
        tableEnv.executeSql(
                "CREATE TABLE output (" +
                "  Season INT, " +
                "  avg_epa DOUBLE " +
                ") WITH (" +
                "  'connector' = 'filesystem', " +
                "  'path' = '/path/to/output.csv', " +
                "  'format' = 'csv'" +
                ")"
        );

        // Insert the results into the output table
        result.executeInsert("output");
    }
}
