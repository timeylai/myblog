var num_last = 3;  //����ȫ�ֱ�������չʾ����������
var urls = location.href;
// console.log(urls);
var temp = urls.split('/');
var content_type = temp[temp.length-1];
//console.log(temp[temp.length-1]);
//var keyboard = document.getElementById("keyboardd");
//console.log(keyboard);
$(window).scroll(function a() {
    //alert("test");
    //var num = 0, num_last = 3 ;
    var windowHeight = $(window).height();//��ǰ���ڵĸ߶�
    var scrollTop = $(window).scrollTop();//��ǰ�������������¹����ľ���
    var docHeight = $(document).height(); //��ǰ������ҳ�ĵ��ĸ߶�
    //console.log(scrollTop, windowHeight, docHeight);
    //�� ��������ײ��ľ��� + �����������ľ��� >= �ĵ��ĸ߶� - ���ڵĸ߶�
    //�������������ľ��� + ���ڵĸ߶� = ��ǰ�����ĵ��߶ȣ�  ����ǻ����Ĺ�ʽ
    if (scrollTop + windowHeight >= docHeight-3) {
        //console.log("begin");
        $.ajax({
            type: "POST",
            url:"/type/blog",
            data:{num:"true",num_last:num_last, content_type:content_type},
            dataType: 'json',  //  json ��̨���ص���json��ʽ���ݣ�js����json��������.
            success:function (data) {
                //console.log(data);
                $(document).ready(function () {
                    var str ="";
                    for (var i = 0; i < data.length; i++) {
                        str = "    <li> <span class=\"blogpic\"><a href=\"p/"+data[i].page_id +"\"><img src=\""+data[i].content_img +"\"></a></span>\n" +
                            "      <h3 class=\"blogtitle\"><a href=\"p/"+data[i].page_id +"\" target=\"_blank\">"+ data[i].content_title+"</a></h3>\n" +
                            "      <div class=\"bloginfo\">\n" +
                            "          <p><a href=\"p/"+data[i].page_id +"\"  target=\"_blank\">"+data[i].content_page +"</a></p>\n" +
                            "      </div>\n" +
                            "      <div class=\"autor\"><span class=\"lm\"><a href=\"/\" title=\"CSS3|Html5\" target=\"_blank\" class=\"classname\">CSS3|Html5</a></span><span class=\"dtime\">"+data[i].content_time +"</span>" +
                            "<span class=\"viewnum\">"+data[i].see +"</span><span class=\"readmore\"><a href=\"p/"+data[i].page_id +"\" target=\"_blank\">read more</a></span></div>\n" +
                            "    </li>";
                        $(".blogs").append(str)

                    }
                })
            }
        });
        num_last = num_last+3;
        // console.log(num_last)
     }
});

