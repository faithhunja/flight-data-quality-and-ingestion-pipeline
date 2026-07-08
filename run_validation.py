import great_expectations as gx

try:
    # Connect to the version-controlled context files
    context = gx.get_context(mode="file")
    
    # Retrieve and run the checkpoint
    checkpoint = context.checkpoints.get("my_checkpoint")
    print("Executing Great Expectations validation gate...")
    result = checkpoint.run()
    
    # Handle data metrics evaluation state
    if not result.success:
        print("Data Quality Gate Failed! Anomaly detected inside live_flights.csv.")
        exit(1) # Crashes the GitHub action step
        
    print("All Quality Gates Passed! Telemetry data matches clean expectations.")
    exit(0)

except Exception as e:
    print(f"Failed to execute data quality checks: {e}")
    exit(1)