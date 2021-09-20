$(document).ready(function(){
	var dropZone = $('#upload-container');

	$('#file-input').focus(function() {
		$('label').addClass('focus');
	})
	.focusout(function() {
		$('label').removeClass('focus');
	});


	dropZone.on('drag dragstart dragend dragover dragenter dragleave drop', function(){
		return false;
	});

	dropZone.on('dragover dragenter', function() {
		dropZone.addClass('dragover');
	});

	dropZone.on('dragleave', function(e) {
		let dx = e.pageX - dropZone.offset().left;
		let dy = e.pageY - dropZone.offset().top;
		if ((dx < 0) || (dx > dropZone.width()) || (dy < 0) || (dy > dropZone.height())) {
			dropZone.removeClass('dragover');
		}
	});

	dropZone.on('drop', function(e) {
		dropZone.removeClass('dragover');
		let files = e.originalEvent.dataTransfer.files;
		sendFiles(files);
	});

	$('#file-input').change(function() {
		let files = this.files;
		sendFiles(files);
	});

    function UserException(message) {
       this.message = message;
       this.name = "Исключение, определённое пользователем";
    }

	function sendFiles(files) {
	    let maxFileSize = 5242880;
		let Data = new FormData();
		$(files).each(function(index, file) {
		    if ((file.size <= maxFileSize) && (file.type == 'text/plain')) {
                Data.append('files', file);
			}
			else {
			    alert('Неверное расширение и/или размер файла!');
			     throw new UserException('');
			}
		});

		$.ajax({
			url: dropZone.attr('action'),
			type: dropZone.attr('method'),
			data: Data,
			contentType: false,
			processData: false,
			success: function(data) {
			    if (data.hasOwnProperty('primary_key')) {
                    var primary_key = data.primary_key;
                    if (primary_key != null) {
				        alert('Файл был успешно загружен!');
				        window.location.href  = '/file/' + primary_key
                    }
                    else {
                        alert('Файл не был загружен!');
                    }
                }
			}
		});
	}
})