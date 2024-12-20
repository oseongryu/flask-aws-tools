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
                    const ipList = $('#ip_list');
                    ipList.empty();
    
                    data.forEach((item, index) => {
                        const li = $('<p></p>').text(`${index + 1}. ${item.name}: ${item.ip}`);
                        ipList.append(li);
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
                    const deployList = $('#deploy_list');
                    deployList.empty();
    
                    data.forEach((item, index) => {
                        const li = $('<p></p>').text(`${index + 1}. ${item.displaytime}: ${item.deploymentGroupName} ${item.status}`);
                        deployList.append(li);
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
                success: function(data) {
                    const checkList = $('#check_list');
                    checkList.empty();
                    data.forEach(item => {
                        const li = $('<p></p>').text(item);
                        checkList.append(li);
                    });
                },
                error: function(error) {
                    console.error('Error:', error);
                }

            });
        }
    }
})();

