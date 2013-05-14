    $(function() {
      $( "#searchText" ).autocomplete({
        source: function( request, response ) {
          $.ajax({
            url: "http://localhost:8080/suggest",
            dataType: "jsonp",
            data: {
              query: request.term
            },
            success: function( data ) {
              response( $.map( data.result, function( item ) {
                return {
                  label: item.name,
                  value: item.name,
                  desc: item.tag
                }
              }));
            }
          });
        },
        minLength: 2,
        select: function( event, ui ) {
          console.log('Selected');
          console.log(ui.item);
          if (ui.item) {
            $("#query").val(ui.item.label);
            $("#tag").val(ui.item.desc);
          }
         },
        open: function() {
          $( this ).removeClass( "ui-corner-all" ).addClass( "ui-corner-top" );
        },
        close: function() {
          $( this ).removeClass( "ui-corner-top" ).addClass( "ui-corner-all" );
        }
      })
      .data( "ui-autocomplete" )._renderItem = function( ul, item ) {
        return $( "<li>" )
          .append( "<a>" + item.label + "<span style=\"float:right;color:#888\">" + item.desc + "</a>" )
          .appendTo( ul );
      };
    });
