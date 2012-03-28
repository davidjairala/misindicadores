// Retorna el valor de scroll del cliente
function getScrollXY() {
	var scrOfX = 0, scrOfY = 0;
	if( typeof( window.pageYOffset ) == 'number' ) {
		//Netscape compliant
		scrOfY = window.pageYOffset;
		scrOfX = window.pageXOffset;
	} else if( document.body && ( document.body.scrollLeft || document.body.scrollTop ) ) {
		//DOM compliant
		scrOfY = document.body.scrollTop;
		scrOfX = document.body.scrollLeft;
	} else if( document.documentElement && ( document.documentElement.scrollLeft || document.documentElement.scrollTop ) ) {
		//IE6 standards compliant mode
		scrOfY = document.documentElement.scrollTop;
		scrOfX = document.documentElement.scrollLeft;
	}
	return [ scrOfX, scrOfY ];
}

// Regresa el tamano de la ventana del usuario
function getUserWindow() {
	if (parseInt(navigator.appVersion)>3) {
		if (navigator.appName=="Netscape") {
			winW = window.innerWidth;
			winH = window.innerHeight;
		}
		if (navigator.appName.indexOf("Microsoft")!=-1) {
			winW = document.body.offsetWidth;
			winH = document.body.offsetHeight;
		}
	}
	return [winW,winH];
}

// Agrega clase de text a todos los textfields
function textClasses() {
  $('input[type=submit]').addClass('button');
  $('input[type=button]').addClass('button');
  
	$('#cont_form input[type=text]').addClass('text');
  
  $('.small input[type=text]').addClass('small');
  $('.small select').addClass('small');
  $('.small input[type=submit]').addClass('small');
  $('.small input[type=button]').addClass('small');
}

// Alterna colores de rows de una tabla
function tableColors() {
	$("tr:even").css("background-color", "#dddddd");
	$("tr:odd").css("background-color", "#ffffff");
	$("table.portada tr").css("background-color", "#ffffff");
	
	$("tr:even").mouseover(function() {
		$(this).css("background-color", "yellow");
	});
	
	$("tr:even").mouseout(function() {
		$(this).css("background-color", "#dddddd");
	});
	
	$("tr:odd").mouseover(function() {
		$(this).css("background-color", "yellow");
	});
	
	$("tr:odd").mouseout(function() {
		$(this).css("background-color", "#ffffff");
	});
}

// Selecciona todos los elementos con una clase
function selectAll(className) {
	var parts = getElementsByClassName(className);
	var i = 0;
	
	while(i < parts.length) {
		parts[i].checked = true;
		
		i++;
	}
}

// Des-selecciona todos los elementos con una clase
function deSelectAll(className) {
	var parts = getElementsByClassName(className);
	var i = 0;
	
	while(i < parts.length) {
		parts[i].checked = false;
		
		i++;
	}
}

// Muestra o esconde un id
function toggle(id) {
	if($('#'+id).css('display') == 'none') {
		$('#'+id).css('display', 'block');
	} else {
		$('#'+id).css('display', 'none');
	}
}

// Se encarga de colorear los avatars
function avatarsColors() {
	$("div.avatars > img").css("border", "2px solid white");
	$("div.avatars > img").mouseover(function() {
		$(this).css('border', '2px solid orange');
	});
	$("div.avatars > img").mouseout(function() {
		$(this).css('border', '2px solid white');
	});
	$("div.avatars > img").click(function() {
		changeAvatar($(this).attr("src"));
	});
}

// Cambia el avatar de un usuario con ajax
function changeAvatar(src) {
	$("#avatar_actual").attr("src", src);
	$.post('/set_avatar', {src:src}, function(msg) {
		info('El avatar se ha cambiado correctamente.');
	});
}

// Activa botones del menu
function menuButtons() {
	$(".a_menu_btn").each(function() {
		var id = $(this).attr("id");
		var part = id.split("_");
		part = part[1];
		
		var id_menu = "menu_" + part;
		
		var offset = $(this).offset();
		
		$("#" + id_menu).css({"left": (offset.left - 6) + "px", "top": (offset.top + 26) + "px"});
		
		$(this).mouseover(function() {
			$("#" + id_menu).css("display", "block");
		});
		
		$("#" + id_menu).mouseover(function() {
			$("#" + id_menu).css("display", "block");
		});
		
		$(this).mouseout(function() {
			$("#" + id_menu).css("display", "none");
		});
		
		$("#" + id_menu).mouseout(function() {
			$("#" + id_menu).css("display", "none");
		});
	});
}

// Arregla PNGs para IE6
function fixPngs() {
	$('body').supersleight();
}

// Shows loading box
function showLoading() {
	$('#loading').centerInClient();
	$('#loading').css("display", "block");
}

// Hides loading box
function hideLoading() {
	$("#loading").fadeOut("fast");
}

// Abre o cierra menu de indicadores
function toggleMenuIndicadores() {
	var src = '';
	toggle('cont_menu_indicadores');
	
	if($('#cont_menu_indicadores').css('display') == 'block') {
		src = $('#img_cont_menu_indicadores').attr('src');
		src = src.split('_');
		src[1] = 'abj';
		src = src.join('_');
		$('#img_cont_menu_indicadores').attr('src', src);
	} else {
		src = $('#img_cont_menu_indicadores').attr('src');
		src = src.split('_');
		src[1] = 'der';
		src = src.join('_');
		$('#img_cont_menu_indicadores').attr('src', src);
	}
}

// Checa que selects mostrar para el boletin
function checkBoletinSelects() {
  var per = $('#boletin_periocidad').val();
  
  if(per == "semanal") {
    $('#cont_dia').css('display', 'block');
    $('#cont_hora').css('display', 'block');
  } else if(per == "diario") {
    $('#cont_dia').css('display', 'none');
    $('#cont_hora').css('display', 'block');
  } else if(per == "dos_dia") {
    $('#cont_dia').css('display', 'none');
    $('#cont_hora').css('display', 'none');
  }
}

// Actualiza widget
function actualizaWidget(url) {
  var secciones = '';
  
  $('input[type=checkbox]').each(
    function() {
      if($(this).attr('checked') == true) {
        secciones += $(this).val() + '|';
      }
    }
	);
  
  var width = $('#iframe_width').val();
  var height = $('#iframe_height').val();
  
  var code_iframe = '<iframe src="'+url+'?m=widgets&c=widget&s='+secciones+'" border="0" frameborder="0" style="border: 2px solid #ccc; width: '+width+'px; height: '+height+'px; margin: 0px; padding: 0px; overflow: auto;" scrolling="yes" horizontalscrolling="no" verticalscrolling="yes"></iframe>';
  
  $('#iframe_cont').html(code_iframe);
  
  $('#code_widget').val(code_iframe);
}

$(document).ready(function() {
	fixPngs();
	tableColors();
	textClasses();
	menuButtons();
});

// Show loading
$().ajaxSend(function(r,s){
	showLoading();
});

// Hide loading
$().ajaxStop(function(r,s){
	hideLoading();
});
