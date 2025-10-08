## Triggers in Azure Data Factory

### Schedule Trigger

- Runs on calendar clock
- Supports periodic and specific times
- Trigger to pipeline is many to many
- Can be scheduled only at a future point in time

### Tumbling Window Trigger

- Runs at periodic intervals
- Windows are fixed size and non overlapping
- Can be scheduled for past windows/slices
- Trigger to pipeline is one to one

### Event Trigger

- Runs in response to events
- Events can be creation or deletion of blobs/files
- Trigger to pipeline is many to many.

