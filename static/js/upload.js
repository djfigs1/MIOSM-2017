var inputs = document.querySelectorAll( '.inputfile' );

Array.prototype.forEach.call( inputs, function( input )
{
	var label	 = document.getElementById('photoLabel')
		labelVal = label.innerHTML;

	input.addEventListener( 'change', function( e )
	{
		var fileName = '';
		fileName = e.target.value.split( '\\' ).pop();
		if( fileName ) {
			label.innerHTML = fileName;
			label.style['background-color'] =  "#09a32d";
		}
		else {
			label.innerHTML = labelVal;
		}
	});
});

function submitPhoto() {
    ga('send', 'event', 'Uploads', 'submit');
}