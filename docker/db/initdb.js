use research

db.submissions.createIndex({user: 1, study: 1}, {unique: true});

db.studies.insert({"name": "Hillary Clinton", "available_places": 3, "user": "123"});
