// Code goes here
var busca = null;
var array = ["Gui Ferreira Code","Dicas de Programação","Você aprende Praticando"] ;

$(document).ready(function(){
  $('#bsuca').bind('input',function(){
    busca = $(this).val().toLowerCase();

    if(busca !== ''){
      var corresponde = false;
      var saida = Array();
      var quantidade = 0;
      for(var key in array){

        corresponde = array[key].toLowerCase().indexOf(busca) >= 0;
        if(corresponde){
          saida.push(array[key]);
          quantidade += 1;
        }
      }
      if(quantidade){
        $('#saidaTxt').text('');
        $('#quantidade').html(quantidade+' resultados!<br><br>');
        for(var ind in saida){
           $('#saidaTxt').append("<li>"+saida[ind]+"</li>"+"<br>");
        }

      }else{
        $('#quantidade').html('');
        $('#saidaTxt').text('Nenhum resultado...');
      }

    }else{
      $('#quantidade').html('');
      $('#saidaTxt').text('Nenhum resultado...');
    }



  });
});
