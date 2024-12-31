package com.example.flink;

import org.apache.flink.table.api.TableEnvironment;
import org.apache.flink.table.api.EnvironmentSettings;
import org.apache.flink.table.api.TableResult;
import org.apache.flink.table.delegation.ExecutorFactory;

public class NFLDataProcessor {
    public static void main(String[] args) throws Exception {
        // Check if DDL is passed as an argument
        if (args.length == 0) {
            throw new IllegalArgumentException("No DDL provided. Pass the DDL as an argument.");
        }

        // Capture the DDL from the command-line argument
        String ddl = args[0];

        // Set up the Table Environment in Batch Mode
        EnvironmentSettings settings = EnvironmentSettings.newInstance()
                .inBatchMode() // Batch mode
                .build();
        TableEnvironment tableEnv = TableEnvironment.create(settings);

        // Execute the provided DDL
        tableEnv.executeSql(ddl);

        // Perform a query on the table
        TableResult result = tableEnv.executeSql(
                "SELECT Season, AVG(EPA) as avg_epa " +
                "FROM nfl_data " +
                "GROUP BY Season"
        );

        // Print the result
        result.print();
    }
}
