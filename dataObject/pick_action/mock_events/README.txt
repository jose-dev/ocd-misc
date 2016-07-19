PICK DATA OBJECTS
---------------------
    
    python generate_pick_do.py > pick_DO.json
    gsutil cp pick_DO.json gs://testjunk-pick-action/
    bq load --source_format=NEWLINE_DELIMITED_JSON mock_pick_action.pick_dataObject_001 gs://testjunk-pick-action/pick_DO.json ../schemas/pick_dataObject.schema 
