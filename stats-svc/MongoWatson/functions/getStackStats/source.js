exports = function(arg){

  var collection = context.services.get("mongodb-atlas").db("mongowatson").collection("stacks");

  var stack = arg.stackFrames;
  var rawinput = arg.rawinput;

  var now = new Date();

  return collection.findOneAndUpdate(
      { stack },
      {
        $set: { lastSeen: now },
        $setOnInsert: { firstSeen: now },
        $inc: { occurrences: 1 },
      },
      { upsert: true, returnNewDocument: true, projection: { stack: 0 } }
    ).then(doc => {
      //console.log(doc);

      context.services.get("mongodb-atlas").db("mongowatson").collection("rawinputs").updateOne( { rawinput, stack: doc._id },
        {
          $set: { lastSeen: now },
          $setOnInsert: { firstSeen: now },
          $inc: { occurrences: 1 }
        }, { upsert: true } )

      return doc;
    })
};
