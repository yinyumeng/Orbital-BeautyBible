$(function(){
  $(".delete").click(function(evt){
    evt.preventDefault();
    console.log(evt);
    var ele = $(evt.target);
    console.log(ele.attr("key"))    ;
    ele.parent(".textarea3").slideUp(400, function() {$(this).remove();});
    $.post('/delete_article',{article_key:ele.attr("key")});   
  });
   $("#delete").click(function(evt){
    evt.preventDefault();
    console.log(evt);
    var ele = $(evt.target);
    console.log(ele.attr("key"))    ;
    ele.parent(".field4").slideUp(400, function() {$(this).remove();});
    $.post('/delete_item',{item_key:ele.attr("key")});   
  });
    $("#delete_product").click(function(evt){
    evt.preventDefault();
    console.log(evt);
    var ele = $(evt.target);
    console.log(ele.attr("key"))    ;
    ele.parent(".field3").slideUp(400, function() {$(this).remove();});
    $.post('/delete_product',{product_key:ele.attr("key")});   
  });
  
})
