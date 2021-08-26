var loadingMsgIndex,
    botui = new BotUI('stars-bot'),
    API = 'http://127.0.0.1:5000/response?userid=123&input=';

function getResponse(input, cb) {
  if (['cls', 'clear', 'clear screen','reload','refresh'].includes(input)){ 
    location.reload();
    return null;
  }
  var xhr = new XMLHttpRequest();
  var self = this;
  xhr.open('GET', API+input);
  xhr.onload = function () {
    console.log(xhr.responseText)
    responseText = JSON.parse(xhr.responseText)
    if(responseText.debug){
      console.log("Debugg")
      responseText = JSON.stringify(responseText)
    }
    else{
      responseText = responseText.response
    }
    cb(responseText);
  }
  xhr.send();
}

function init() {
    botui.action.text({
      delay: 1000,
      action: {
        value: '',
        placeholder: ''
      }
    })
    .then(function (res) {
    loadingMsgIndex = botui.message.bot({
      delay: 200,
      loading: true
    }).then(function (index) {
      loadingMsgIndex = index;
      getResponse(res.value, printResponse)
    });
  });
}

function printResponse(stars) {
  botui.message
  .update(loadingMsgIndex, {
    content: '' + (stars || "0") + ''
  })
  .then(init); // ask again for repo. Keep in loop.
}

botui.message.add({
  content: 'Hello I am Heimdall, how can I help you!'
});

init();
