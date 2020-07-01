function verifyNames() {
  actorOne = document.getElementById('actor-one');
  actorTwo = document.getElementById('actor-two');
  $.ajax({
    type: "GET",
    url: "/degrees.py",
    success: callbackFunc
  });
  console.log('got here...');
}

function callbackFunc(response) {
  // do something with the response
  console.log(response);
}

