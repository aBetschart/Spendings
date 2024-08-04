function insertTodaysDate(textfield) {
  var today = new Date();
  var day = String(today.getDate()).padStart(2, '0');
  var month = String(today.getMonth() + 1).padStart(2, '0');
  var year = today.getFullYear();
  
  var today = year + "-" + month + "-" + day
  textfield.value = today
}


  