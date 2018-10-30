$(document).ready(function(){ /*llamamos a la funcion y hacemos referencia al documento*/
    
    $('.icon-arriba').click(function(){ /*esta funcion permite hacer referencia a la imagen que se utiliza para ir arriba*/
        $('body, html').animate({ 
            scrollTop: '0px'
        }, 500);
    } );
    
    $(window).scroll(function(){
        if($(this).scrollTop()>0){
           $('.icon-arriba').slideDown(400);
           }
        else{
           $('.icon-arriba').slideUp(400); 
        }
    } );
} );