var user_viewer = user_viewer || (function(){
    var console = window.console || {log:function(){},error:function(){},warn:function(){}};
    // console.log(this.document.currentScript.src);
    return{
        init: function(e){
            console.log(this.document.currentScript.src);
        },
        grid : function(e){
            var msnry = new Masonry( '.grid', {
                itemSelector: '.grid-item',
                columnWidth: '.grid-sizer',
                percentPosition: true,
                gutter : 5,
            });
            imagesLoaded('.grid').on( 'progress', function() {
                msnry.layout();
            });
            var viewer = new Viewer(document.querySelector('.grid'), {
                navbar : false,
                toolbar : false,
                url: 'data-original',
                title : function(image, imageData) { return image.title; },
                view(event) {
                    event.detail.image.title = event.detail.originalImage.title;
                },
            });
        },
        clean: function (){
            $(".grid").remove();
            var imageView  = document.getElementById('imageView');

            var elDivGrid = document.createElement('div')
            elDivGrid.setAttribute('class', 'grid')
            imageView.appendChild(elDivGrid);

            var elDivGridSizer = document.createElement('div')
            elDivGridSizer.setAttribute('class', 'grid-sizer')
            elDivGrid.appendChild(elDivGridSizer)
        },
    }
})();

