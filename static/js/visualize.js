function submit_form(){
    var hello_selector = document.querySelector(".hello");
    //console.log(hello_selector.innerHTML);
    var selected_instance = document.getElementById("type").value;
    //console.log(typeof selected_instance);
    if (selected_instance ==="0"){
        error = document.querySelector(".error");
        error.innerText = "Select other options.";
    }
    url  = return_url(selected_instance);
    console.log(url);
}
function return_url(selected_instance){
    let url = ""
    switch(selected_instance){
        case "1":
            url = "/visualization/credit-history/";
            new_url = `http://127.0.0.1:8000${url}`;
            console.log(new_url);   
            fetch_cr_history(new_url);
            break
        case "2":
            url = "/visualization/loan-prediction/";
            new_url = `http://127.0.0.1:8000${url}`;
            console.log(new_url);   
            fetch_prediction(new_url);
            break;
        case "3":
            url = "/visualization/home-ownership/"
            new_url = `http://127.0.0.1:8000${url}`;
            console.log(new_url);
            fetch_home_ownership(new_url);
            break;
        case "4":
            url = "/visualization/loan-intent/"
            new_url = `http://127.0.0.1:8000${url}`;
            console.log(new_url);
            fetch_loan_intent(new_url);
            break;
    }
    // return url;
}
function fetch_data(url){
    console.log(url);
    fetch(url)
    .then(response => response.json())
    .then(data => manipulate(data))

}
function fetch_cr_history(url){
    console.log(url);
    fetch(url)
    .then(response => response.json())
    .then(data => manipulate_cr_history(data))
}
function fetch_prediction(url){
    console.log(url);
    fetch(url)
    .then(response => response.json())
    .then(data => manipulate_prediction(data))
}
function fetch_home_ownership(url){
    console.log(url);
    fetch(url)
    .then(response => response.json())
    .then(data => manipulate_home_ownership(data))
}
function fetch_loan_intent(url){
    console.log(url);
    fetch(url)
    .then(response => response.json())
    .then(data => manipulate_loan_intent(data))
}
function manipulate(data){
    console.log(data);
    }
function manipulate_cr_history(data){
    let chartStatus = Chart.getChart("myChart"); // <canvas> id
    if (chartStatus != undefined) {
        chartStatus.destroy();
    }
    const ctx = document.getElementById('myChart');
    console.log(data['credit_history']);
    arr = []
    console.log(typeof data['credit_history']);
    // console.log(data['credit_history'].keys());
    instances = Object.keys(data['credit_history']);
    values = Object.values(data['credit_history']);
    var myChart = new Chart(ctx, {
      type:'doughnut',
      data: {
        labels: instances,
        datasets: [{
        //   label: 'Number of Loans',
          data: values,
          backgroundColor: [
            'rgba(255, 99, 132, 0.2)',
            'rgba(75, 192, 192, 0.2)',
            'rgba(153, 102, 255, 0.2)'
          ],
          borderColor: [
            'rgb(255, 99, 132)',
            'rgb(75, 192, 192)',
            'rgb(153, 102, 255)'
          ], 
          borderWidth: 1
        }],
        
      },
    });
    document.querySelector(".chart-info").innerText = "Doughnut Chart of Credit History (in years).";
    error = document.querySelector(".error");
    error.style.display = "none";
    // myChart.destroy();
}

function manipulate_prediction(data){
    let chartStatus = Chart.getChart("myChart"); // <canvas> id
    if (chartStatus != undefined) {
        chartStatus.destroy();
    }
    const ctx = document.getElementById('myChart');
    console.log(data['loan_prediction']);
    arr = []
    console.log(typeof data['loan_prediction']);
    // console.log(data['credit_history'].keys());
    instances = Object.keys(data['loan_prediction']);
    values = Object.values(data['loan_prediction']);
    new Chart(ctx, {
      type: 'bar',
      data: {
        labels: instances,
        datasets: [{
          label: 'Number of Loans',
          data: values,
          backgroundColor: [
            'rgba(255, 99, 132, 0.2)',
            'rgba(75, 192, 192, 0.2)',
            'rgba(153, 102, 255, 0.2)'
          ],
          borderColor: [
            'rgb(255, 99, 132)',
            'rgb(75, 192, 192)',
            'rgb(153, 102, 255)'
          ], 
          borderWidth: 1
        }],
        
      },
      options: {
        scales: {
          y: {
            beginAtZero: true
          }
        }
      }
    });
    document.querySelector(".chart-info").innerText = "Bar Chart of Loan Approvals.";
    error = document.querySelector(".error");
    error.style.display = "none";
}

function manipulate_loan_intent(data){
    let chartStatus = Chart.getChart("myChart"); // <canvas> id
    if (chartStatus != undefined) {
        chartStatus.destroy();
    }
    const ctx = document.getElementById('myChart');
    console.log(data['loan_intent']);
    arr = []
    console.log(typeof data['loan_intent']);
    // console.log(data['credit_history'].keys());
    instances = Object.keys(data['loan_intent']);
    values = Object.values(data['loan_intent']);
    new Chart(ctx, {
      type: 'polarArea',
      data: {
        labels: instances,
        datasets: [{
        //   label: 'Number of Loans',
          data: values,
          backgroundColor: [
            'rgba(255, 99, 132, 0.2)',
            'rgba(75, 192, 192, 0.2)',
            'rgba(153, 102, 255, 0.2)',
            'rgba(255, 205, 86, 0.2)',
            'rgba(75, 192, 192, 0.2)'
          ],
          borderColor: [
            'rgb(255, 99, 132)',
            'rgb(75, 192, 192)',
            'rgb(153, 102, 255)'
          ], 
          borderWidth: 1
        }],
        
      },
    });
    document.querySelector(".chart-info").innerText = "Pie Chart of Home Ownership";
    error = document.querySelector(".error");
    error.style.display = "none";
}

function manipulate_home_ownership(data){
    let chartStatus = Chart.getChart("myChart"); // <canvas> id
    if (chartStatus != undefined) {
        chartStatus.destroy();
    }
    const ctx = document.getElementById('myChart');
    console.log(data['home_ownership']);
    arr = []
    console.log(typeof data['home_ownership']);
    // console.log(data['credit_history'].keys());
    instances = Object.keys(data['home_ownership']);
    values = Object.values(data['home_ownership']);
    new Chart(ctx, {
      type: 'pie',
      data: {
        labels: instances,
        datasets: [{
        //   label: 'Number of Loans',
          data: values,
          backgroundColor: [
            'rgba(255, 99, 132, 0.2)',
            'rgba(75, 192, 192, 0.2)',
            'rgba(153, 102, 255, 0.2)',
            'rgba(255, 205, 86, 0.2)',
            'rgba(75, 192, 19, 0.2)',
            'rgba(25,13,25,0.2)',
          ],
          borderColor: [
            'rgb(255, 99, 132)',
            'rgb(75, 192, 192)',
            'rgb(153, 102, 255)'
          ], 
          borderWidth: 1
        }],
        
      },
    });
    document.querySelector(".chart-info").innerText = "Pie Chart of Home Ownership";
    error = document.querySelector(".error");
    error.style.display = "none";
}