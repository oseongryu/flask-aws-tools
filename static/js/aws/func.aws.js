var func_aws = func_aws || (function(){
    var console = window.console || {log:function(){},error:function(){},warn:function(){},dir:function(){}};
    console.dir(this.document.currentScript.src);
    return{
        init: function(e){
            console.dir(this.document.currentScript.src);
        },
        search_ip: async function(event) {
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
        },
        search_deploy: async function(event) {
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
        },
        search_alb_download: async function(event) {
            const checkList = document.getElementById('checkList');
            const formData = checkList.getFormData();
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
        }
    }
})();

