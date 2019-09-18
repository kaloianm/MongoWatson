exports = function(fnname, payload){
  if (!payload.body) return {ok: false, error:"no body"};

  var body = {};
  try {
    body = EJSON.parse(payload.body.text());
  } catch (e) {
    return {ok: false, error:"malformed body"};
  }
  return context.functions.execute(fnname, body);
};