success:function (data) {
                console.log(data);
                var str ="";
                for (var i=0; i<data.length; i++) {
                    $(document).ready(bloghtml())
                }
            }

            function bloghtml() {
    $(".blogs").html(
        "    <li> <span class=\"blogpic\"><a href=\"/\"><img src=\"../images/other/text01.jpg\"></a></span>\n" +
        "      <h3 class=\"blogtitle\"><a href=\"p/"+data[i].page_id +"\" target=\"_blank\">"+data[i].conetent_title +"</a></h3>\n" +
        "      <div class=\"bloginfo\">\n" +
        "          <p><a href=\"p/"+data[i].page_id +"\"  target=\"_blank\">"+ data[i].conetent+"</a></p>\n" +
        "      </div>\n" +
        "      <div class=\"autor\"><span class=\"lm\"><a href=\"/\" title=\"CSS3|Html5\" target=\"_blank\" class=\"classname\">CSS3|Html5</a></span><span class=\"dtime\">"+ data[i].see+"</span><span class=\"viewnum\">ä¯ÀÀ£¨{{ i['see'] }}£©</span><span class=\"readmore\"><a href=\"p/{{ i['page_id'] }}\" target=\"_blank\">ÔÄ¶ÁÔ­ÎÄ</a></span></div>\n" +
        "    </li>"
    )
}