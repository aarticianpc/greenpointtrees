$(window).load(function(){
	$('.close-sidebar').click(function(){
		$('.sidebar').hide();
		$('.toggle-sidebar-btn').show();
	});
	$('.toggle-sidebar-btn').click(function(){
		$('.sidebar').show();
		$('.toggle-sidebar-btn').hide();
	});
})