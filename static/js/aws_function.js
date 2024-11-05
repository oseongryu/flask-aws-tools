// static/js/select_hours.js
$(document).ready(function() {
  var today = new Date();
  today.setDate(today.getDate() - 7);
  var formattedDate = today.toISOString().split('T')[0];
  $('#date').val(formattedDate);

  $('#search_ip').click(function(event) {
      event.preventDefault();
      const filterValue = $('#filter_value').val();
      $.ajax({
          url: '/aws/run_aws_ip',
          method: 'POST',
          contentType: 'application/json',
          data: JSON.stringify({ filter_value: filterValue }),
          success: function(data) {
              const devList = $('#dev_list');
              const prdList = $('#prd_list');
              devList.empty();
              prdList.empty();

              data.dev.forEach(item => {
                  const li = $('<li></li>').text(item);
                  devList.append(li);
              });

              data.prd.forEach(item => {
                  const li = $('<li></li>').text(item);
                  prdList.append(li);
              });
          },
          error: function(error) {
              console.error('Error:', error);
          }
      });
  });

  $('#search_deploy').click(function(event) {
    event.preventDefault();
    const searchDate = $('#date').val();
    console.log('searchDate:', searchDate);
    $.ajax({
        url: '/aws/run_aws_deploy',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ searchDate: searchDate }),
        success: function(data) {
            console.log('data:', data);
            const resultsContainer = $('#results');
            resultsContainer.empty(); // Clear previous results

            data.forEach(item => {
                const resultItem = `
                    <div class="result-item">
                        <p>- ${item.displaytime}: ${item.deploymentGroupName} ${item.status}</p>
                    </div>
                `;
                resultsContainer.append(resultItem);
            });
        },
        error: function(error) {
            console.error('Error:', error);
        }
    });
});

});