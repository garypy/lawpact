$(document).ready(function() {
	var uploader = new plupload.Uploader({ //实例化一个plupload上传对象
											browse_button : 'browse',
											url : 'url',
											flash_swf_url : 'https://cdn.bootcss.com/plupload/2.1.7/Moxie.swf',
											filters : {
												mime_types : [
													{title : "Image files", extensions : "jpg,gif,png"}
												],
												max_file_size : '100kb',
												prevent_duplicates : true
											},
											multi_selection : false
										});
	uploader.init(); //初始化

	//绑定文件添加进队列事件
	uploader.bind('FilesAdded',function(uploader,files){
		$('#preview').empty();
		for(var i = 0; i<files.length; i++)
		{
			var file_name = files[i].name; //文件名
			//构造html来更新UI
			$('<p class="file-name">' + file_name + '</p>').appendTo('#preview');
			!function(i){
				previewImage(files[i],function(imgsrc){
					$('<img src="'+ imgsrc +'" />').appendTo('#preview');
				})
		    }(i);
		}
	});

	uploader.bind('Error',function(uploader,errObject){
		$('#preview').empty();

		switch (errObject.code)
		{
		case (-600):
			var index = $('<div class="alert alert-warning alert-dismissible fade in" role="alert"></div>').appendTo('#preview');
			$('<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>').appendTo(index);
			$('<p><strong>出错了！</strong>图片太大，超过100kb无法上传T_T</p>').appendTo(index);
			break;
		}
	});

	$('#start_upload').click(function(event) {
		uploader.start();
	});
});

function previewImage(file,callback){//file为plupload事件监听函数参数中的file对象,callback为预览图片准备完成的回调函数
	if(!file || !/image\//.test(file.type)) return; //确保文件是图片
	if(file.type=='image/gif'){//gif使用FileReader进行预览,因为mOxie.Image只支持jpg和png
		var fr = new mOxie.FileReader();
		fr.onload = function(){
			callback(fr.result);
			fr.destroy();
			fr = null;
		}
		fr.readAsDataURL(file.getSource());
	}else{
		var preloader = new mOxie.Image();
		preloader.onload = function() {
			//preloader.downsize( 300, 300 );//先压缩一下要预览的图片,宽300，高300
			var imgsrc = preloader.type=='image/jpeg' ? preloader.getAsDataURL('image/jpeg',100) : preloader.getAsDataURL(); //得到图片src,实质为一个base64编码的数据
			callback && callback(imgsrc); //callback传入的参数为预览图片的url
			preloader.destroy();
			preloader = null;
		};
		preloader.load( file.getSource() );
	}	
}
	
