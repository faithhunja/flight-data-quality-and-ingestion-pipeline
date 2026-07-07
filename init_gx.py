import os
import great_expectations as gx
import great_expectations.expectations as gxe

# Initialize file-system context (creates the local configs)
context = gx.get_context(mode="file")

# Add or update a pandas data source targeting local directories
data_source = context.data_sources.add_or_update_pandas(name="flight_data_source")

# Define a data asset pointing directly to the csv
os.makedirs("data", exist_ok=True)
if not os.path.exists("data/live_flights.csv"):
    with open("data/live_flights.csv", "w") as f:
        f.write("icao24,callsign,longitude,latitude,baro_altitude,on_ground,velocity\n")

asset_name = "live_flights_asset"
if asset_name in [asset.name for asset in data_source.assets]:
    data_asset = data_source.get_asset(name=asset_name)
else:
    data_asset = data_source.add_csv_asset(
        name=asset_name, 
        filepath_or_buffer="data/live_flights.csv"
    )

# Set up a batch definition to pull the entire file during runs
batch_definition = data_asset.add_batch_definition_whole_dataframe(
    name="all_flights_batch"
)

# Create an expectation suite & define data quality rules
suite_name = "flight_quality_suite"
suite = gx.ExpectationSuite(name=suite_name)

# Assertions (core data quality rules)
suite.add_expectation(gxe.ExpectColumnValuesToNotBeNull(column="icao24"))
suite.add_expectation(gxe.ExpectColumnValuesToNotBeNull(column="latitude"))
suite.add_expectation(gxe.ExpectColumnValuesToNotBeNull(column="longitude"))
suite.add_expectation(gxe.ExpectColumnValuesToBeOfType(column="velocity", type_="float64"))

# Save or update suite in the data context
context.suites.add_or_update(suite)

# Build a validation definition (to bind batch & suite)
validation_definition = gx.ValidationDefinition(
    name="flight_validation_def",
    data=batch_definition,
    suite=suite
)

# Save or update validation definition to the context
validation_definition = context.validation_definitions.add_or_update(validation_definition)

# Build and save checkpoint gate using validation definition
checkpoint_name = "my_checkpoint"
checkpoint = gx.Checkpoint(
    name=checkpoint_name,
    validation_definitions=[validation_definition],  # Plural array structure
    actions=[
        gx.checkpoint.UpdateDataDocsAction(name="update_all_data_docs") # Compiles the HTML Docs
    ]
)

context.checkpoints.add_or_update(checkpoint)
print("Great Expectations initialized successfully! Configuration files generated.")