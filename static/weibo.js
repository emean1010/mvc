// WEIBO API
// 获取所有 weibo
var apiWeiboAll = function(callback) {
    var path = '/api/weibo/all'
    ajax('GET', path, '', callback)
//    r = ajax('GET', path, '', callback)
//    callback(r)
}

var apiWeiboAdd = function(form, callback) {
    var path = '/api/weibo/add'
    ajax('POST', path, form, callback)
}

var apiWeiboDelete = function(weiboId, callback) {
    var path = `/api/weibo/delete?id=${weiboId}`
    ajax('GET', path, '', callback)
}

var apiWeiboUpdate = function(form, callback) {
    var path = `/api/weibo/update`
    ajax('POST', path, form, callback)
}

var apiCommentAdd = function(form, callback) {
    var path = '/api/weibo/comment_add'
    ajax('POST', path, form, callback)
}

var apiCommentDelete = function(weiboId, comment, callback) {
    var path = `/api/weibo/comment_delete?id=${weiboId}&comment=${comment}`
    ajax('GET', path, '', callback)
}

//评论更新的api
var apiCommentUpdate = function(form, callback) {
    var path = `/api/weibo/comment_update`
    ajax('POST', path, form, callback)
}

var weiboTemplate = function(weibo, commentsTemplate) {
    var w = `
       <div class="weibo-cell" data-id="${weibo.id}">
       <span class="weibo-title">${weibo.content}</span>
       <button class="weibo-edit">编辑</button>
       <button class="weibo-delete">删除</button>

       <input type="text" class="input-comment">
       <button class="comment-add">添加评论</button>
       <div class="comment-list">${commentsTemplate}</div>
        </div>
    `
    return w
}

// 添加编辑按钮
var commentsTemplate = function(comments) {
    var cs = ``
    for(var key in comments){
        var c = `
            <div class="comment-cell">
                <span class="comment-content">${comments[key]}</span>
                <button class="comment-edit">编辑</button>
                <button class="comment-delete">删除</button>
            </div>
        `
        cs = cs + c
    }
    return cs
}

var weiboUpdateTemplate = function(content) {
    var t = `
        <div class="weibo-update-form">
            <input class="weibo-update-input" value="${content}"/>
            <button class="weibo-update">更新</button>
        </div>
    `
    return t
}

//构造评论更新输入框和按钮
var commentUpdateTemplate = function(content) {
    var t = `
        <div class="comment-update-form">
            <input class="comment-update-input" value="${content}"/>
            <button class="comment-update">更新</button>
        </div>
    `
    return t
}

var insertWeibo = function(weibo) {
    var comments = weibo.comment
    var weiboCell = weiboTemplate(weibo, commentsTemplate(comments))
    // 插入 weibo-list
    var weiboList = e('#id-weibo-list')
    weiboList.insertAdjacentHTML('beforeend', weiboCell)
}

var insertUpdateForm = function(content, weiboCell) {
    var updateForm = weiboUpdateTemplate(content)
    weiboCell.insertAdjacentHTML('beforeend', updateForm)
}

//插入评论更新框和按钮
var insertUpdateComment = function(content, commentCell) {
    var updateForm = commentUpdateTemplate(content)
    commentCell.insertAdjacentHTML('beforeend', updateForm)
}

var loadWeibos = function() {
    // 调用 ajax api 来载入数据
    apiWeiboAll(function(weibos) {
        log('load all weibos', weibos)
        // 循环添加到页面中
        for(var i = 0; i < weibos.length; i++) {
            var weibo = weibos[i]
            insertWeibo(weibo)
        }
    })
    // second call
}

var bindEventWeiboAdd = function() {
    var b = e('#id-button-add')
    // 注意, 第二个参数可以直接给出定义函数
    b.addEventListener('click', function(){
        var input = e('#id-input-weibo')
        var content = input.value
        log('click add', content)
        var form = {
            content: content,
        }
        apiWeiboAdd(form, function(weibo) {
            // 收到返回的数据, 插入到页面中
            insertWeibo(weibo)
        })
    })
}

//删除之前，先验证返回的message信息
var bindEventWeiboDelete = function() {
    var weiboList = e('#id-weibo-list')
    // 事件响应函数会传入一个参数 就是事件本身
    weiboList.addEventListener('click', function(event) {
    log(event)
    // 我们可以通过 event.target 来得到被点击的对象
    var self = event.target
    log('被点击的元素', self)
    // 通过比较被点击元素的 class
    // 来判断元素是否是我们想要的
    // classList 属性保存了元素所有的 class
    log(self.classList)
    if (self.classList.contains('weibo-delete')) {
        log('点到了删除按钮')
        var weiboId = self.parentElement.dataset['id']
        apiWeiboDelete(weiboId, function(r) {
            log('apiWeiboDelete', r.message)
            // 删除 self 的父节点
            if (r.message == '不是微博作者没有权限') {
                alert(r.message)
            } else {
                self.parentElement.remove()
                alert(r.message)
            }
        })
    } else {
        log('点到了 weibo cell')
    }
})}

var bindEventWeiboEdit = function() {
    var weiboList = e('#id-weibo-list')
    // 事件响应函数会传入一个参数 就是事件本身
    weiboList.addEventListener('click', function(event) {
    log(event)
    // 我们可以通过 event.target 来得到被点击的对象
    var self = event.target
    log('被点击的元素', self)
    // 通过比较被点击元素的 class
    // 来判断元素是否是我们想要的
    // classList 属性保存了元素所有的 class
    log(self.classList)
    if (self.classList.contains('weibo-edit')) {
        log('点到了编辑按钮', self)
        var weiboCell = self.closest('.weibo-cell')
        var weiboId = weiboCell.dataset['id']
        var weiboSpan = e('.weibo-title', weiboCell)
        var content = weiboSpan.innerText
        insertUpdateForm(content, weiboCell)
    } else {
        log('点到了 weibo cell')
    }
})}

var bindEventWeiboUpdate = function() {
    var weiboList = e('#id-weibo-list')
    // 事件响应函数会传入一个参数 就是事件本身
    weiboList.addEventListener('click', function(event) {
    log(event)
    // 我们可以通过 event.target 来得到被点击的对象
    var self = event.target
    log('被点击的元素', self)
    // 通过比较被点击元素的 class
    // 来判断元素是否是我们想要的
    // classList 属性保存了元素所有的 class
    log(self.classList)
    if (self.classList.contains('weibo-update')) {
        log('点到了更新按钮')
        var weiboCell = self.closest('.weibo-cell')
        var weiboId = weiboCell.dataset['id']
        var weiboInput = e('.weibo-update-input', weiboCell)
        var content = weiboInput.value
        var form = {
            id: weiboId,
            content: content,
        }

        apiWeiboUpdate(form, function(weibo) {
            log('apiWeiboUpdate', weibo)

            if (weibo.message == '不是微博作者没有权限') {
                alert(weibo.message)
            } else {
                var weiboSpan = e('.weibo-title', weiboCell)
                weiboSpan.innerText = weibo.content
                var updateForm = e('.weibo-update-form', weiboCell)
                updateForm.remove()
                alert('更新成功')
            }
        })
    } else {
        log('点到了 weibo cell')
    }
})}

var bindEventWeiboAddComment = function() {
    var weiboList = e('#id-weibo-list')
    weiboList.addEventListener('click', function(event) {
    log(event)
    var self = event.target
    log('被点击的元素', self)
    log(self.classList)
    if (self.classList.contains('comment-add')) {
        log('点到了添加评论按钮')
        var weiboCell = self.closest('.weibo-cell')
        var weiboId = weiboCell.dataset['id']
        var commentInput = e('.input-comment', weiboCell)
        var comment = commentInput.value
        var form = {
            id: weiboId,
            comment: comment,
        }

        apiCommentAdd(form, function() {
            var commentsCell = `
                <div class="comment-cell">
                    <span class="comment-content">${comment}</span>
                    <button class="comment-edit">编辑</button>
                    <button class="comment-delete">删除</button>
                </div>
            `
            weiboCell.insertAdjacentHTML('beforeend', commentsCell)
        })
    } else {
        log('点到了 weibo cell')
    }
})}

var bindEventCommentDelete = function() {
    var weiboList = e('#id-weibo-list')
    weiboList.addEventListener('click', function(event) {
    log(event)
    var self = event.target
    log('被点击的元素', self)
    log(self.classList)
    if (self.classList.contains('comment-delete')) {
        log('点到了评论删除按钮')
        var commentCell = self.closest('.comment-cell')
        var commentSpan = commentCell.querySelector('span')
        var comment = commentSpan.innerText
        log('要删除的评论内容', comment)
        var weiboCell = self.parentElement.closest('.weibo-cell')
        var weiboId = weiboCell.dataset['id']
        log('上级微博', weiboCell)

        apiCommentDelete(weiboId, comment, function(r) {
            log('apiCommentDelete', r.message)
            // 删除 self 的父节点
            if (r.message == '不是评论或者微博作者没有权限') {
                alert(r.message)
            } else {
                self.parentElement.remove()
                alert(r.message)
            }
        })
    } else {
        log('点到了 weibo cell')
    }
})}

//绑定评论编辑函数
var bindEventCommentEdit = function() {
    var weiboList = e('#id-weibo-list')
    weiboList.addEventListener('click', function(event) {
    log(event)
    var self = event.target
    log('被点击的元素', self)
    log(self.classList)
    if (self.classList.contains('comment-edit')) {
        log('点到了评论编辑按钮', self)
        var commentCell = self.closest('.comment-cell')
        var commentSpan = e('.comment-content', commentCell)
        var content = commentSpan.innerText
        insertUpdateComment(content, commentCell)
    } else {
        log('点到了 weibo cell')
    }
})}

//绑定评论更新函数
var bindEventCommentUpdate = function() {
    var weiboList = e('#id-weibo-list')
    weiboList.addEventListener('click', function(event) {
    log(event)
    var self = event.target
    log('被点击的元素', self)
    log(self.classList)
    if (self.classList.contains('comment-update')) {
        log('点到了评论更新按钮')
        var commentCell = self.closest('.comment-cell')
        var commentSpan = commentCell.querySelector('span')
        var comment = commentSpan.innerText
        log('要更新的评论内容', comment)
        var weiboCell = self.parentElement.closest('.weibo-cell')
        var weiboId = weiboCell.dataset['id']
        var commentInput = e('.comment-update-input', commentCell)
        var newComment = commentInput.value
        var form = {
            id: weiboId,
            comment: comment,
            newComment: newComment,
        }

        apiCommentUpdate(form, function(comment) {
            log('apiCommentUpdate', comment)

            if (comment.message == '不是评论或者微博作者没有权限') {
                alert(comment.message)
            } else {
                var commentSpan = e('.comment-content', commentCell)
                commentSpan.innerText = comment.content
                var updateForm = e('.comment-update-form', commentCell)
                updateForm.remove()

                alert('更新评论成功')
            }
        })
    } else {
        log('点到了 weibo cell')
    }
})}

var bindEvents = function() {
    bindEventWeiboAdd()
    bindEventWeiboDelete()
    bindEventWeiboEdit()
    bindEventWeiboUpdate()
    bindEventWeiboAddComment()
    bindEventCommentDelete()
    bindEventCommentEdit()
    bindEventCommentUpdate()
}

var __main = function() {
    bindEvents()
    loadWeibos()
}

__main()
