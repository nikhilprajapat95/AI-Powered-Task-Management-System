document.addEventListener("DOMContentLoaded", function () {
  if (typeof workloadData !== "undefined" && workloadData.labels && workloadData.values) {
    const ctx = document.getElementById('workloadChart').getContext('2d');

    new Chart(ctx, {
      type: 'bar',
      data: {
        labels: workloadData.labels,
        datasets: [{
          label: 'Tasks per User',
          data: workloadData.values,
          backgroundColor: 'rgba(54, 162, 235, 0.6)',
          borderColor: 'rgba(54, 162, 235, 1)',
          borderWidth: 1
        }]
      },
      options: {
        responsive: true,
        scales: {
          y: {
            beginAtZero: true,
            ticks: {
              precision: 0
            }
          }
        }
      }
    });
  }
});

