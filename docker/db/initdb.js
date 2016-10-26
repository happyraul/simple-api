use research

db.submissions.createIndex({user: 1, study: 1}, {unique: true});
