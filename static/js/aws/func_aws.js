// static/js/select_hours.js
$(document).ready(function() {
    var today = new Date();
    today.setDate(today.getDate() - 5);
    var formattedDate = today.toISOString().split('T')[0];
    $('#date').val(formattedDate);
    $('#albDate').val(new Date().toISOString().split('T')[0]);

    for (let hour = 1; hour < 24; hour++) {
        $('.hours-list').append(
            `<label><input type="checkbox" name="hours" value="${hour}"> ${hour}</label>`
        );
    }

    $('#btn_search_ip').click(function(event) {
        event.preventDefault();
        const filterValue = $('#filter_value').val();
        $.ajax({
            url: '/aws/run-aws-ip',
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

    $('#btn_search_deploy').click(function(event) {
        event.preventDefault();
        const searchDate = $('#date').val();
        console.log('searchDate:', searchDate);
        $.ajax({
            url: '/aws/run-aws-deploy',
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
  
    $('#selectAll').change(function() {
        $('input[name="hours"]').prop('checked', this.checked);
    });

    $('#selectAllCheckbox').click(function() {
        var isChecked = $(this).prop('checked');
        $('input[name="hours"]').prop('checked', isChecked);
    });

    $('#btn_download').click(function(event) {
        event.preventDefault();
        var formData = $('#hoursForm').serialize();
        $.ajax({
            type: 'POST',
            url: '/aws/run-aws-alb',
            data: formData,
            success: function(response) {
                $('.result').html(response);
            },
            error: function(error) {
                console.error('Error:', error);
            }
        });
    });

});