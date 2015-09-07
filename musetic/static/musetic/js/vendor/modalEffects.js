/**
 * modalEffects.js v1.0.0
 * http://www.codrops.com
 *
 * Licensed under the MIT license.
 * http://www.opensource.org/licenses/mit-license.php
 *
 * Copyright 2013, Codrops
 * http://www.codrops.com
 */
var ModalEffects = (function() {

	function init() {

		var overlay = document.querySelector( '.m-overlay' );

		[].slice.call( document.querySelectorAll( '.m-trigger' ) ).forEach( function( el, i ) {

			var modal = document.querySelector( '#' + el.getAttribute( 'data-modal' ) ),
				close = modal.querySelector( '.m-close' );

			function removeModal( hasPerspective ) {
				classie.remove( modal, 'm-show' );

				if( hasPerspective ) {
					classie.remove( document.documentElement, 'm-perspective' );
				}
			}

			function removeModalHandler() {
				removeModal( classie.has( el, 'm-setperspective' ) );
			}

			el.addEventListener( 'click', function( ev ) {
				classie.add( modal, 'm-show' );
				overlay.removeEventListener( 'click', removeModalHandler );
				overlay.addEventListener( 'click', removeModalHandler );

				if( classie.has( el, 'm-setperspective' ) ) {
					setTimeout( function() {
						classie.add( document.documentElement, 'm-perspective' );
					}, 25 );
				}
			});

			close.addEventListener( 'click', function( ev ) {
				ev.stopPropagation();
				removeModalHandler();
			});

		} );

	}

	init();

})();