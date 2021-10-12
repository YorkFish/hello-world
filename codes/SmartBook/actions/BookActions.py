# coding: utf-8
"""
图书管理模块的 actions

author: York
date: 2021-10-07
"""

from api.PublicApi import *
from models.BookinfoModel import Bookinfo, BookinfoDAO
from models.BorrowregModel import Borrowreg, BorrowregDAO
from models.UserinfoModel import UserinfoDAO
from pages.BookAddPage import BookAddPage
from pages.BookListPage import BookListPage
from pages.BorrowListPage import BorrowListPage


@logincheck
def book_list(page):
    """进入图书列表页面"""
    BookListPage(user=page.user, home=page, prev=page).show()


@authcheck
def book_register(page):
    """进入图书等级页面"""
    BookAddPage(user=page.user, home=page.home_page, prev=page).show()


@authcheck
def do_register(page):
    """登记图书"""
    bookname = get_input(message="请输入书名：", check_re=r"^\w{1,30}$")
    print(f"书名：《{bookname}》")

    for key, val in Bookinfo.BOOK_TYPES.items():
        print(f"{key}-{val}")
    msg = f"请选择分类({'/'.join(Bookinfo.BOOK_TYPES.keys())})："
    regex = f"^{'|'.join(Bookinfo.BOOK_TYPES.keys())}$"
    booktype = get_input(message=msg, check_re=regex)
    logger.debug(f"图书分类为：{booktype}")

    # 输入作者
    author = get_input(message="请输入作者：", check_re=r"^\w{2,10}$")
    logger.debug(f"作者是：{author}")

    print('*' * 50)
    print("您输入的信息如下：")
    print("书名：" + bookname)
    print("分类：" + Bookinfo.BOOK_TYPES[booktype])
    print("作者：" + author)
    print('*' * 50)

    confirm = get_input(message="确认(Y)，取消(N)，重输(R)：",
                        check_re=r"^[ynrYNR]$")
    if confirm.lower() == 'n':
        # 回到图书浏览页面
        page.prev_page.show()
    elif confirm.lower() == 'r':
        page.show()
    elif confirm.lower() == 'y':
        try:
            # 构造一本新书
            book = Bookinfo()
            book.bookname = bookname
            book.author = author
            book.booktype = booktype
            book.is_borrow = False
            book.createuser = page.user.username

            # 将图书存入文件
            BookinfoDAO.insert(book)

            confirm = get_input(message="登记成功...结束(Q)，继续(Enter)",
                                check_re=r"^[qQ]$", empty=True)
            if confirm.lower() == 'q':
                BookListPage(page.user).show()
            else:
                page.show()
        except Exception as e:
            logger.exception(e)
            input(f"{e}...按任意键继续")


@logincheck
def do_booklist(page):
    # 展示查询条件
    # 可以按书名/分类/借阅状态
    command = get_input(message="查询条件：书名(N)，分类(T)，借阅状态(P)，回车查全部:",
                        warning="输入有误...",
                        check_re=r"^[ntpNTP]$", empty=True)
    logger.debug(command)
    if not command or command.lower() in ['n', 't', 'p']:
        if command.lower() == 'n':
            bookname = get_input(message="请输入书名:",
                                 warning="输入有误，请重新输入...")
        if command.lower() == 't':
            print("图书分类:")
            for key, val in Bookinfo.BOOK_TYPES.items():
                print(f"[{key}]-{val}")
            booktype = get_input(message=f"请选择分类({'/'.join(Bookinfo.BOOK_TYPES.keys())}):",
                                 check_re=f"^{'|'.join(Bookinfo.BOOK_TYPES.keys())}$")
        if command.lower() == 'p':
            is_borrow = get_input(message="请选择（空闲(Z)/借阅(B)）:",
                                  warning="输入有误，请重新输入...",
                                  check_re=r"^[ZBzb]$")

        books = BookinfoDAO.select(p_state="normal")
        print("-" * page.MESSAGE_MAX_LEN)
        print("{0:4s}| {1:32s}| {2:8s}| {3:4s}".format("编号", "书名", "分类", "借阅"))
        print("-" * page.MESSAGE_MAX_LEN)
        
        count = 0
        for book in books:
            if command:
                if command.lower() == 'n' and bookname not in book.bookname:
                    continue
                if command.lower() == 't' and book.booktype != booktype:
                    continue
                if command.lower() == 'p':
                    if book.is_borrow and is_borrow.lower() == 'z':
                        continue
                    if not book.is_borrow and is_borrow.lower() == 'b':
                        continue

            bookname_length = 34 - (len(book.bookname.encode('gbk')) - len(book.bookname))
            r_booktype = Bookinfo.BOOK_TYPES.get(book.booktype, "")
            r_is_borrow = "√" if book.is_borrow else ""
            fmt = "{0:6s}| {1:{4}s}| {2:6s}| {3:^4s}"
            print(fmt.format(str(book.id), book.bookname, r_booktype,
                             r_is_borrow, bookname_length))
            count += 1
        print("-" * page.MESSAGE_MAX_LEN)
        print(f"总记录: {count} 条")
        input("......任意键继续......")
        page.show()
    else:
        # 进入图书详情页面
        pass


@logincheck
def do_borrow(page):
    """图书借阅"""
    book_id = get_input(message="请输入要借阅的图书编号：", check_re=r"^\d+$")
    book = BookinfoDAO.select_one(p_id=int(book_id))
    if book is None or book.state == Bookinfo.BOOK_STATUS["DELETE"]:
        input("图书不存在...")
        page.show()
    if book.is_borrow:
        input("图书已经借出...")
        page.show()

    print('*' * 50)
    print("您输入的信息如下：")
    print("书名：" + book.bookname)
    print("分类：" + Bookinfo.BOOK_TYPES[book.booktype])
    print("作者：" + book.author)
    print('*' * 50)

    # 确认
    confirm = get_input(message="确认(Y)，取消(N)：", check_re=r"^[ynYN]$")
    if confirm.lower() == 'y':
        # 登记借阅信息
        # 1. 谁借的书、借阅的时间
        # TODO
        borrow = Borrowreg(bookid=book.id, borrowuserid=page.user.userid)
        BorrowregDAO.insert(borrow)
        
        # 2. 将图书的状态改为“被借阅”
        book.is_borrow = True
        BookinfoDAO.update(book)
        input("借阅登记成功...按任意键继续")

    page.show()


@authcheck
def do_delete(page):
    book_id = get_input(message="请输入要删除的图书编号：", warning="输入有误...",
                        check_re=r"^\d+$")
    book = BookinfoDAO.select_one(p_id=int(book_id))
    if book is None or book.state != Bookinfo.BOOK_STATUS["NORMAL"]:
        input(f"编号({book_id})的图书不存在....")
        page.show()
    if book.is_borrow:
        input(f"未归还的图书不能删除...")
        page.show()

    print("=" * 50)
    print("您要删除的图书信息如下：")
    print("编号：", book.id)
    print("书名：", book.bookname)
    print("分类：", Bookinfo.BOOK_TYPES[book.booktype])
    print("作者：", book.author)
    print("=" * 50)

    # 接收确认结果
    confirm = get_input(message="确认删除(Y)，取消(N)：", warning="输入有误...",
                        check_re=r"^[ynYN]$")
    logger.debug(f"确认结果：{confirm}")
    if confirm.lower() == 'y':
        # 1.修改图书信息，将状态改为删除
        book.state = Bookinfo.BOOK_STATUS["DELETE"]
        BookinfoDAO.update(book)
        input("删除成功...按任意键继续")
    page.show()


@authcheck
def do_modify(page):
    book_id = get_input(message="请输入要修改的图书编号：", warning="输入有误...",
                        check_re=r"^\d+$")
    book = BookinfoDAO.select_one(p_id=int(book_id))
    if book is None or book.state != Bookinfo.BOOK_STATUS["NORMAL"]:
        input(f"编号({book_id})的图书不存在...")
        page.show()

    print("=" * 50)
    print("原图书信息如下：")
    print("书名：", book.bookname)
    print("分类：", Bookinfo.BOOK_TYPES[book.booktype])
    print("作者：", book.author)
    print("=" * 50)

    print("(请输入要修改的内容，不修改直接回车)")
    # 接收书名
    bookname = get_input(message="请输入新的书名：", check_re=r"^(\w){1,30}$",
                         empty=True)
    logger.debug(f"书名：《{bookname}》")

    # 接收类型
    print("图书分类")
    for key, val in Bookinfo.BOOK_TYPES.items():
        print(f"[{key}]-{val}")
    booktype = get_input(message=f"请选择新分类({'/'.join(Bookinfo.BOOK_TYPES.keys())}):",
                         check_re=f"^{'|'.join(Bookinfo.BOOK_TYPES.keys())}$",
                         empty=True)
    logger.debug(f"输入分类：{booktype}")

    # 接收作者
    author = get_input(message="请输入新作者：", check_re=r"^(\w){2,10}$",
                       empty=True)
    logger.debug(f"确认作者：{author}")

    if bookname or booktype or author:
        print("=" * 50)
        print("您输入的信息如下：")
        if bookname:
            print(f"新书名：《{bookname}》")
        if booktype:
            print("新分类：", Bookinfo.BOOK_TYPES[booktype])
        if author:
            print("新作者：", author)
        print("=" * 50)

        # 接收确认结果
        confirm = get_input(message="确认修改(Y)，取消(N)：",
                            warning="输入有误...", check_re=r"^[ynYN]$")
        logger.debug(f"确认结果：{confirm}")

        if confirm.lower() == 'y':
            # 1.修改图书信息
            if bookname:
                book.bookname = bookname
            if booktype:
                book.booktype = booktype
            if author:
                book.author = author
            BookinfoDAO.update(book)
            input("修改成功...按任意键继续")
    else:
        print("未输入任何新内容，不做修改")
    page.show()


@logincheck
def book_borrowlist(page):
    """跳转至借阅清单页面"""
    BorrowListPage(user=page.user, home=page, prev=page).show()


@authcheck
def book_reader_borrowlist(page):
    """跳转至借阅清单页面"""
    # 注意：这里是查看读者的借阅，而不是管理员自己的
    BorrowListPage(user=page.user, home=page.home_page, prev=page,
                   reader=page.reader).show()


@logincheck
def do_borrowlist(page):
    if page.reader:
        if not page.user.is_admin:
            input("无权查看他人信息...按任意键继续")
            page.home_page.show()
        borrows = BorrowregDAO.select(p_borrow_user_id=page.reader.userid)
    else:
        borrows = BorrowregDAO.select(p_borrow_user_id=page.user.userid)

    print('-' * page.MESSAGE_MAX_LEN)
    print("{:6}|{:22}|{:12}|{:4}".format("借阅编号", "书名", "借阅人", "状态"))
    print('-' * page.MESSAGE_MAX_LEN)

    count = 0
    for reg in borrows:
        user = UserinfoDAO.select_one(p_userid=reg.borrow_user_id)
        book = BookinfoDAO.select_one(p_id=reg.book_id)
        bookname_length = 24 - (len(book.bookname.encode("gbk")) - len(book.bookname))
        reg_state_str = "借出" if reg.state == 'B' else "归还"
        print("{0:<10}|{1:{4}}|{2:15}|{3:4}".format(
            reg.id, book.bookname, user.username, reg_state_str,
            bookname_length))
        count += 1
    
    print('-' * page.MESSAGE_MAX_LEN)
    print(f"总记录：{count}条")
    input(f"...按任意键继续...")
    page.prev_page.show()


@logincheck
def do_return(page):
    """归还图书"""
    reg_id = get_input(message="请输入要归还的图书的借阅编号：", check_re=r"^\d+$")
    reg = BorrowregDAO.select_one(p_id=int(reg_id))

    # 检查 有借阅记录，还未归还，为管理员，本人归还
    if reg is None or reg.state == 'B' or (page.user.is_admin or 
            reg.borrow_user_id == page.user.userid):
        reg.state = Borrowreg.BORROW_STATUS["RETURN"]
        reg.return_user_id = page.user.userid
        BorrowregDAO.update(reg)

        # 注意：要同时更新图书状态
        book = BookinfoDAO.select_one(p_id=reg.book_id)
        book.is_borrow = False
        BookinfoDAO.update(book)

        input("图书归还成功...按任意键退出")
    else:
        input("无权归还...按任意键退出")
    page.show()
