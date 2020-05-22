$(function () {
    const emptyMessage = '没有未读通知';
    const notice = $('#notifications'); //notifications_list.html

    // 点击铃铛时，检查 最近的消息通知
    function CheckNotifications() {
        $.ajax({
            url: '/notifications/latest-notifications/',
            cache: false,
            success: function (data) {
                // 如果消息不为空
                if (!data.includes(emptyMessage)) {
                    // 为铃铛添加样式  显示为红色
                    notice.addClass('btn-danger');
                }
            },
        });
    }

    CheckNotifications();  // 页面加载时执行

    function update_social_activity(id_value) {
        // 通过标签选择器更新那一条消息的 评论数 与赞数
        // new_single.html  line 3 传递的news.uuid
        const newsToUpdate = $('[news-id=' + id_value + ']');
        $.ajax({
            url: '/news/update-interactions/',
            data: {'id_value': id_value},
            type: 'POST',
            cache: false,
            success: function (data) {
                $(".like-count", newsToUpdate).text(data.likes);
                $(".comment-count", newsToUpdate).text(data.comments);
            },
        });
    }

    // 点击铃铛时显示 消息
    notice.click(function () {
        // 如果弹窗已显示
        if ($('.popover').is(':visible')) {
            // 隐藏窗口
            notice.popover('hide');
            // 再次检查最近通知
            CheckNotifications();
        } else {
            notice.popover('dispose');
            $.ajax({
                url: '/notifications/latest-notifications/',
                cache: false,
                success: function (data) {
                    notice.popover({
                        html: true, //加载html框
                        trigger: 'focus',
                        container: 'body',
                        placement: 'bottom',
                        content: data,
                    });
                    notice.popover('show');
                    notice.removeClass('btn-danger')
                },
            });
        }
        return false;  // 不是False  不进行跳转
    });

    // WebSocket连接，使用wss(https)或者ws(http)
    const ws_scheme = window.location.protocol === 'https:' ? 'wss' : 'ws';
    const ws_path = ws_scheme + '://' + window.location.host + '/ws/notifications/';
    const ws = new ReconnectingWebSocket(ws_path);

    // 监听后端发送过来的消息
    ws.onmessage = function (event) {
        // 将接收到的消息 JSON化
        const data = JSON.parse(event.data);
        switch (data.key) {
            case "notification":  //消息通知
                if (currentUser !== data.actor_name) {  // 消息提示的发起者不提示
                    notice.addClass('btn-danger');
                }
                break;

            case "social_update": // 用户点赞
                if (currentUser !== data.actor_name) {
                    notice.addClass('btn-danger');
                }
                update_social_activity(data.id_value);  // 获取新的赞数 与评论数
                break;

            case "additional_news": // 其他用户发送新动态
                if (currentUser !== data.actor_name) {
                    $('.stream-update').show(); // new_list.html line22
                }
                break;

            default:
                console.log('error', data);
                break;
        }
    };
});
