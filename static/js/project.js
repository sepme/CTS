$(document).ready(function () {

    // init save clipboard
    $(".js-copy-clipboard").click(function () {
        if ($(this).hasClass("input-group-text")) {
            let input = $(this).closest(".input-group").find("input")[0];
            input.select();
            input.setSelectionRange(0, 99999);
            document.execCommand("copy");
            iziToast.success({
                rtl: true,
                message: "کد پروژه با موفقیت کپی شد!",
                position: 'bottomLeft'
            });
        }
    });

    //****************************************//
    //  Deadline Progress
    //****************************************//
    let addDeadlineForm = $("form#add-card-ajax");
    if (addDeadlineForm.length) {
        addDeadlineForm.submit(function (event) {
            event.preventDefault();
            let title = addDeadlineForm.find("#id_card_title").val();
            let due = addDeadlineForm.find("#id_card_deadline").val();
            $.ajax({
                method: "POST",
                url: "/addCard/",
                data: addDeadlineForm.serialize(),
                success: function (data) {
                    console.log(data);
                    let progressItem = `<div class="step-container">
                                    <span class="step-date">
                                        <div>${due}</div>
                                    </span>
                                    <span class="step-name">${title}</span>
                                </div>`;
                    $(progressItem).insertBefore('.project-progress .line-100');
                    $("#addDeadline").modal("hide");
                    iziToast.success({
                        rtl: true,
                        message: "آیتم با موفقیت اضافه شد!",
                        position: 'bottomLeft'
                    });
                },
                error: function (data) {
                    console.log(data);
                    iziToast.error({
                        rtl: true,
                        message: "درخواست شما با مشکل مواجه شد!\nلطفا دوباره تکرار کنید.",
                        position: 'bottomLeft'
                    });
                }
            });
        });
    }

    let deadLineProgress = $(".project-progress.project-progress-sm");
    if (deadLineProgress.length) {
        if ($(window).width() < 992) {
            let deadLineProgressOverFlow = deadLineProgress.closest(".overflow-auto");
            if (deadLineProgressOverFlow.find(".project-progress").offset().left <= deadLineProgressOverFlow.offset().left - 50) {
                deadLineProgressOverFlow.prev(".scroll-left").removeClass("d-none");
            }
            deadLineProgressOverFlow.scroll(function () {
                if ($(this).find(".project-progress").offset().left > $(this).offset().left - 50) {
                    $(this).prev(".scroll-left").addClass("d-none");
                } else {
                    $(this).prev(".scroll-left").removeClass("d-none");
                }

                let rightPos = $(this).find(".project-progress").offset().left + $(this).find(".project-progress").outerWidth();
                let fixRightPos = $(this).offset().left + $(this).outerWidth();
                if (rightPos - fixRightPos < 50) {
                    $(this).next(".scroll-right").addClass("d-none");
                } else {
                    $(this).next(".scroll-right").removeClass("d-none");
                }
            });
            let w_diff = deadLineProgress.outerWidth() - deadLineProgressOverFlow.outerWidth() - deadLineProgressOverFlow.offset().left;
            deadLineProgressOverFlow.prev(".scroll-left").click(function () {
                let scrollAmount = $(this).next(".overflow-auto").find(".project-progress").offset().left * -1 - w_diff - deadLineProgressOverFlow.outerWidth();
                $(this).next(".overflow-auto").animate({scrollLeft: scrollAmount}, 300);
            });
            deadLineProgressOverFlow.next(".scroll-right").click(function () {
                let scrollAmount = $(this).prev(".overflow-auto").find(".project-progress").offset().left * -1 - w_diff + deadLineProgressOverFlow.outerWidth();
                $(this).prev(".overflow-auto").animate({scrollLeft: scrollAmount}, 300);
            });
        }
    }
    //****************************************//
    //  End Deadline Progress
    //****************************************//

    //****************************************//
    //  Task Bar
    //****************************************//
    let taskList = $(".ct-checklist");
    let addTaskForm = $("form#add-task-ajax");
    if (taskList.length) {

        addTaskForm.find(".ct-task-assignee.ct-option-btn .dropdown-item").each(function () {

        });

        let involved_users = [];

        addTaskForm.find(".ct-task-assignee.ct-option-btn .dropdown-item").each(function () {
            let data = {
                "username": $(this).attr("data-value"),
                "fullname": $(this).find("img").attr("alt"),
                "photo": $(this).find("img").attr("src")
            };
            involved_users.push(data);
        });

        // Function to get task values => (pk, text, due, assigns)
        function get_task_values(task) {
            let taskText = task.find(".ct-checklist-item__detail .ct-checklist__text .task-description").text();

            let taskDue = null;
            if (task.find(".ct-checklist-item__detail").hasClass("has-due")) {
                taskDue = task.find(".ct-checklist-item__detail .ct-checklist-item-due button span").text();
            }

            let taskAssigns = [];
            task.find(".ct-checklist-item__detail .ct-checklist__text .atMention").each(function () {
                taskAssigns.push($(this).text());
            });

            return {
                'pk': task.attr("data-value"),
                'text': taskText,
                'due': taskDue,
                'assigns': taskAssigns,
            };
        }

        // Function to get pending task values => (pk, text, due, assigns)
        function get_pending_task_values(task) {
            let taskText = task.find(".ct-checklist-item__detail .ct-checklist__pre pre").text();

            let taskDue = null;
            if (task.find(".ct-checklist-item__footer .ct-task-due span").text() !== "") {
                taskDue = task.find(".ct-checklist-item__footer .ct-task-due span").text();
            }

            let taskAssigns = [];
            task.find(".ct-checklist-item__footer .ct-task-assignee .dropdown div.dropdown-item.selected").each(function () {
                taskAssigns.push($(this).attr("data-value"));
            });

            return {
                'pk': task.attr("data-value"),
                'text': taskText,
                'due': taskDue,
                'assigns': taskAssigns,
            };
        }

        // check task is change
        function is_change(task) {
            let taskValues = get_task_values(task);
            let pendingTaskValues = get_pending_task_values(task);
            if (taskValues.text !== pendingTaskValues.text || taskValues.due !== pendingTaskValues.due || taskValues.assigns.length !== pendingTaskValues.assigns.length) {
                return true;
            }
            $.each(taskValues.assigns, function (key, value) {
                let index = $.inArray(value, pendingTaskValues.assigns);
                if (index === -1) {
                    return true;
                }
            });
            return false;
        }

        // Show task assignments
        function show_task_assignments(task, assigns) {
            let facePile = task.find(".ct-checklist-item__footer .ct-task-assignee ul.facepile-list");
            let maxItem = 4;
            if ($(window).width() < 420) {
                maxItem = 1;
            } else if ($(window).width() < 500) {
                maxItem = 3;
            }
            facePile.html("");
            let moreMembers = ``;
            for (let i = 0; i < assigns.length; i++) {
                let item = {};
                for (let j = 0; j < involved_users.length; j++) {
                    if (assigns[i].replace("@", "") === involved_users[j].username) {
                        item = {
                            'username': involved_users[j].username,
                            'fullname': involved_users[j].fullname,
                            'photo': involved_users[j].photo
                        };
                        break;
                    }
                }

                if (i < maxItem) {
                    facePile.append(`<li class="member" data-value="${item.username}">
                        <div class="dropdown">
                            <img src="${item.photo}"
                                alt=""
                                width="32px"
                                class="dropdown-toggle"
                                data-toggle="dropdown"
                                aria-haspopup="true"
                                aria-expanded="false">
                            <div class="dropdown-menu">
                                <div class="py-1 px-4 facepile-detail d-flex">
                                    <img src="${item.photo}"
                                        alt=""
                                        width="50px">
                                    <div class="ml-2">
                                        <div class="full-name text-right">${item.fullname}</div>
                                        <div class="uuid">@${item.username}</div>
                                    </div>
                                </div>
                                <div class="dropdown-divider"></div>
                                <a class="dropdown-item text-center danger-item delete-user"
                                href="javascript: void(0);">
                                    حذف از
                                    لیست
                                    <i class="fas fa-user-times float-inline-end"></i>
                                </a>
                            </div>
                        </div>
                    </li>`);
                } else {
                    moreMembers += `
                        <li class="py-1 px-4 facepile-detail d-flex" data-value="${item.username}">
                            <a class="mr-2 text-center danger-item py-3 delete-user"
                                href="javascript: void(0);">
                                <i class="fas fa-times"></i>
                            </a>
                            <div class="mr-2">
                                <div class="full-name text-right">
                                    ${item.fullname}
                                </div>
                                <div class="uuid">
                                    @${item.username}
                                </div>
                            </div>
                            <img src="${item.photo}"
                                alt=""
                                width="50px">
                        </li>
                    `;
                }
                facePile.closest(".ct-task-assignee")
                    .find(`.dropdown div.dropdown-item[data-value='${item.username}']`).addClass("selected");
            }

            if (maxItem < assigns.length) {
                facePile.append(`
                    <li class="more-member">
                        <div class="dropdown">
                            <button class="btn-default dropdown-toggle no-arrow"
                                data-toggle="dropdown"
                                aria-haspopup="true"
                                aria-expanded="false">
                                +${assigns.length - maxItem}
                            </button>
                            <ul class="dropdown-menu">
                                ${moreMembers}        
                            </ul>
                        </div>
                    </li>`);
            }

            facePile.find(".delete-user").click(function () {
                let taskItem = $(this).closest("li");
                facePile.closest(".ct-task-assignee")
                    .find(`.dropdown div.dropdown-item[data-value='${taskItem.attr("data-value")}']`).removeClass("selected");
                let taskValues = get_pending_task_values(task);
                show_task_assignments(task, taskValues.assigns);
            });
        }

        // Show task edititing front 
        function show_task_edit(task) {

            // Save open task in pendingTasks and hidden that
            let openTask = taskList.find(".ct-checklist__item.onEdit");
            if (openTask.length) {
                if (is_change(openTask)) {
                    openTask.addClass("draft");
                }

                openTask.removeClass("onEdit");
                openTask.find(".ct-checklist-item__footer").addClass("d-none");
                openTask.find(".ct-checklist-item__detail .ct-checklist__pre")
                    .addClass("d-none");
                openTask.find(".ct-checklist-item__detail .ct-checklist__text")
                    .removeClass("d-none")
            }


            // <If> exists is True use pendingTasks detail in edit <Else> use saved detail 
            let taskValues = {};
            if (task.hasClass("draft")) {
                taskValues = get_pending_task_values(task);
            } else {
                taskValues = get_task_values(task);
            }
            console.log(taskValues);
            let taskText = taskValues.text;
            let taskDue = taskValues.due;
            let taskAssigns = taskValues.assigns;

            // Put task values in editing parts
            task.find(".ct-checklist-item__detail .ct-checklist__text").addClass("d-none");
            task.addClass("onEdit");
            task.find(".ct-checklist-item__footer").removeClass("d-none");
            task.find(".ct-checklist-item__footer .ct-task-due span").text(taskDue);
            task.find(".ct-checklist-item__detail .ct-checklist__pre").removeClass("d-none")
                .find("pre").text(taskText);

            // Show assigns
            show_task_assignments(task, taskAssigns);

        }

        // edit task
        function init_task_options(taskItem) {
            taskItem.find(".ct-checklist-item__detail .ct-checklist-item__control .ct-checklist-item-edit").click(function () {
                let checklistItem = $(this).closest(".ct-checklist__item");

                show_task_edit(checklistItem);

                // edit task mention users
                checklistItem.find(".ct-checklist-item__footer .ct-task-assignee.ct-option-btn div.dropdown-item").click(function () {
                    if (!$(this).hasClass("selected")) {
                        $(this).addClass("selected");
                        let taskValues = get_pending_task_values(checklistItem);
                        show_task_assignments(checklistItem, taskValues.assigns);
                    }
                });

                // init cancel editing btn
                checklistItem.find(".ct-checklist-item__footer button.cancel-change").click(function () {
                    checklistItem.removeClass("onEdit draft");
                    let taskValues = get_task_values(checklistItem);
                    checklistItem.find(".ct-checklist-item__detail .ct-checklist__text .task-description").text(taskValues.text);
                    checklistItem.find(".ct-checklist-item__detail .ct-checklist-item-due button span").text(taskValues.due);
                    checklistItem.find(".ct-checklist-item__detail .ct-checklist__text").removeClass("d-none");
                    checklistItem.find(".ct-checklist-item__detail .ct-checklist__pre").addClass("d-none");
                    checklistItem.find(".ct-checklist-item__footer").addClass("d-none");
                });
                // init save edit btn
                checklistItem.find(".ct-checklist-item__footer button.save-change").click(function () {
                    // TODO: Send new task data to server
                    let data = {
                        "delete": true,
                        "pk": checklistItem.attr("data-value")
                    };
                    $.ajax({
                        method: "POST",
                        url: "/addTask/",
                        data: data,
                        success: function (data) {

                        },
                        error: function (data) {

                        }
                    });
                    checklistItem.removeClass("onEdit draft");
                    let taskValues = get_pending_task_values(checklistItem);
                    let assigns = ``;
                    for (let i = 0; i < taskValues.assigns.length; i++) {
                        assigns += ` <span class="atMention d-inline-block me">@${taskValues.assigns[i]}</span>`;
                    }
                    checklistItem.find(".ct-checklist-item__detail .ct-checklist__text .atMention").remove();
                    $(assigns).insertBefore(checklistItem.find(".ct-checklist-item__detail .ct-checklist__text .task-description"));
                    checklistItem.find(".ct-checklist-item__detail .ct-checklist__text .task-description").text(taskValues.text);
                    if (taskValues.due) {
                        checklistItem.find(".ct-checklist-item__detail").addClass('has-due');
                        checklistItem.find(".ct-checklist-item__detail .ct-checklist-item-due").removeClass("d-none");
                        checklistItem.find(".ct-checklist-item__detail .ct-checklist-item-due button span").text(taskValues.due);
                    } else {
                        checklistItem.find(".ct-checklist-item__detail").removeClass('has-due');
                        checklistItem.find(".ct-checklist-item__detail .ct-checklist-item-due").addClass("d-none");
                    }
                    checklistItem.find(".ct-checklist-item__detail .ct-checklist__text").removeClass("d-none");
                    checklistItem.find(".ct-checklist-item__detail .ct-checklist__pre").addClass("d-none");
                    checklistItem.find(".ct-checklist-item__footer").addClass("d-none");

                });
            });
            // init edit task due
            taskItem.each(function () {
                let thisItemBtn = $(`#id_task_due${$(this).attr('data-value')}`);
                thisItemBtn.pDatepicker({
                    format: 'YYYY/MM/DD',
                    onShow: function (unix) {
                        let datePicker = $(".datepicker-container");
                        if (datePicker.find(".datepicker-plot-area").height() + datePicker.offset().top > $(window).height()) {
                            if (datePicker.offset().top > 310) {
                                datePicker.css("top", datePicker.offset().top - 310);
                            } else {
                                datePicker.css("top", 0);
                            }
                        }
                    },
                    dayPicker: {
                        onSelect: function (unix) {
                            let pdate = new persianDate(unix);
                            thisItemBtn.find("span").html(pdate.format("YYYY/MM/DD"));
                        },
                    },
                });
            });
            // delete task
            taskItem.find(".ct-checklist-item-delete").click(function () {
                let deleteItem = $(this);
                let data = {
                    "delete": true,
                    "pk": deleteItem.closest(".ct-checklist__item").attr("data-value")
                };
                $.ajax({
                    method: "POST",
                    url: "/addTask/",
                    data: data,
                    success: function (data) {
                        deleteItem.closest(".ct-checklist__item").remove();
                        // show success toast
                        iziToast.success({
                            rtl: true,
                            message: "تسک با موفقیت حذف شد!",
                            position: 'bottomLeft'
                        });
                    },
                    error: function (data) {
                        console.log(data);
                        iziToast.error({
                            rtl: true,
                            message: data,
                            position: 'bottomLeft'
                        });
                    }
                });
            });
            //check or uncheck task
            taskItem.find(".ct-checklist-item__checkbox input[type='checkbox']").click(function () {
                let checkBox = $(this);
                let data = {
                    "check": checkBox.is(":checked"),
                    "pk": checkBox.closest(".ct-checklist__item").attr("data-value")
                };
                $.ajax({
                    method: "POST",
                    url: "/addTask/",
                    data: data,
                    success: function (data) {
                        if (checkBox.is(":checked")) {
                            let text = checkBox.closest(".ct-checklist__item").find(".ct-checklist-item__detail .ct-checklist__text").html();
                            checkBox.closest(".ct-checklist__item").find(".ct-checklist-item__detail .ct-checklist__text").html(`<del>${text}</del>`);
                        } else {
                            let text = checkBox.closest(".ct-checklist__item").find(".ct-checklist-item__detail .ct-checklist__text del").html();
                            checkBox.closest(".ct-checklist__item").find(".ct-checklist-item__detail .ct-checklist__text").html(`${text}`);
                        }
                        // show success toast
                        iziToast.success({
                            rtl: true,
                            message: "تسک با موفقیت حذف شد!",
                            position: 'bottomLeft'
                        });
                    },
                    error: function (data) {
                        console.log(data);
                        iziToast.error({
                            rtl: true,
                            message: data,
                            position: 'bottomLeft'
                        });
                    }
                });
            });
        }

        init_task_options(taskList.find(".ct-checklist__item"));

        $('#id_task_due').pDatepicker({
            format: 'YYYY/MM/DD',
            onShow: function (unix) {
                let datePicker = $(".datepicker-container");
                if (datePicker.find(".datepicker-plot-area").height() + datePicker.offset().top > $(window).height()) {
                    if (datePicker.offset().top > 310) {
                        datePicker.css("top", datePicker.offset().top - 310);
                    } else {
                        datePicker.css("top", 0);
                    }
                }
            },
            dayPicker: {
                onSelect: function (unix) {
                    let pdate = new persianDate(unix);
                    $('#id_task_due span').html(pdate.format("YYYY/MM/DD"));
                },
            },
        });

        addTaskForm.find(".ct-task-assignee.ct-option-btn .dropdown-item").click(function () {
            if (!$(this).hasClass("selected")) {
                let uuid = $(this).attr("data-value");
                let fullname = $(this).find("img").attr("alt");
                let imgUrl = $(this).find("img").attr("src");
                $(this).addClass("selected");
                addTaskForm.find(".tagId-list").append(`<li class="tagId-item" data-value="${uuid}">
                                                        <div class="relative">
                                                            <img src="${imgUrl}"
                                                                 width="46px" height="46px" class="m-0"
                                                                 alt="${uuid}">
                                                            <svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-x"
                                                                 fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                                                                <path fill-rule="evenodd"
                                                                      d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708z"></path>
                                                            </svg>
                                                        </div>
                                                        <div class="p-1 tagId-item-info">
                                                            <div class="dir-rtl">${fullname}</div>
                                                            <div>@${uuid}</div>
                                                        </div>
                                                    </li>`);
                let thisDropItem = $(this);
                addTaskForm.find(".tagId-list .tagId-item:last-child .relative").click(function () {
                    $(this).closest(".tagId-item").remove();
                    thisDropItem.removeClass("selected");
                });
            }
            // let title = addTaskForm.find("#id_task_title").html();
            // addTaskForm.find("#id_task_title").html(`<span class="atMention me" title="">@${mentionVal}</span>` + title);
        });

        addTaskForm.submit(function (event) {
            event.preventDefault();
            let data = {"project_id": addTaskForm.find("input[name='project_id']").val()};
            let title = addTaskForm.find("#id_task_title").html();
            let deadline = "";
            let dropdown_list = addTaskForm.find(".ct-task-assignee.ct-option-btn .dropdown-menu").html();
            data["description"] = title;
            let mentions = [];
            let mentionsHtml = "";
            addTaskForm.find(".tagId-list .tagId-item").each(function () {
                mentions.push($(this).attr("data-value"));
                mentionsHtml += `<span class="atMention d-inline-block me">@${$(this).attr("data-value")}</span>`;
            });
            data["involved_users"] = mentions;

            if ($('#id_task_due span').html() !== "") {
                deadline = $('#id_task_due').attr("value");
            }
            data["deadline"] = deadline;
            let pk = taskList.find(".ct-checklist__item").length + 1;
            $.ajax({
                method: "POST",
                url: "/addTask/",
                data: data,
                success: function (data) {
                    let task = `
                                <div class="ct-checklist__item" data-value="${pk}">
                                    <div class="ct-checklist-item__checkbox">
                                        <div class="form-group form-check">
                                            <input type="checkbox" class="form-check-input inp-cbx" id="checkList#${pk}" name="requestResearcher" value="1" hidden="">
                                            <label class="form-check-label cbx mb-0" for="checkList#${pk}">
                                            <span>
                                                <svg class="inline-svg bi bi-check2" viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg">
                                                    <path fill-rule="evenodd" d="M13.854 3.646a.5.5 0 0 1 0 .708l-7 7a.5.5 0 0 1-.708 0l-3.5-3.5a.5.5 0 1 1 .708-.708L6.5 10.293l6.646-6.647a.5.5 0 0 1 .708 0z"></path>
                                                </svg>
                                            </span>
                                            </label>
                                        </div>
                                    </div>
                                    <div class="ct-checklist-item__detail ${deadline === '' ? "" : "has-due"}">
                                        <div class="ct-checklist__text">
                                            ${mentionsHtml}
                                            <span class="task-description">${title}</span>
                                        </div>
                                        <div class="ct-checklist__pre d-none">
                                            <pre contenteditable="true"></pre>
                                        </div>
                                        <div class="ct-checklist-item__control d-flex">
                                            <div class="ct-checklist-item-edit">
                                                <button>
                                                    <svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-pencil" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                                                        <path fill-rule="evenodd" d="M12.146.146a.5.5 0 0 1 .708 0l3 3a.5.5 0 0 1 0 .708l-10 10a.5.5 0 0 1-.168.11l-5 2a.5.5 0 0 1-.65-.65l2-5a.5.5 0 0 1 .11-.168l10-10zM11.207 2.5L13.5 4.793 14.793 3.5 12.5 1.207 11.207 2.5zm1.586 3L10.5 3.207 4 9.707V10h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.293l6.5-6.5zm-9.761 5.175l-.106.106-1.528 3.821 3.821-1.528.106-.106A.5.5 0 0 1 5 12.5V12h-.5a.5.5 0 0 1-.5-.5V11h-.5a.5.5 0 0 1-.468-.325z"></path>
                                                    </svg>
                                                </button>
                                            </div>
                                            <div class="ct-checklist-item-delete">
                                                <button>
                                                    <svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-trash" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                                                        <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z"></path>
                                                        <path fill-rule="evenodd" d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4L4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z"></path>
                                                    </svg>
                                                </button>
                                            </div>
                                        </div>
                                        <div class="ct-checklist-item-due ct-option-btn ${deadline === '' ? "d-none" : ""}">
                                            <button>
                                                <span>${deadline}</span>
                                                <svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-clock" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                                                    <path fill-rule="evenodd" d="M8 15A7 7 0 1 0 8 1a7 7 0 0 0 0 14zm8-7A8 8 0 1 1 0 8a8 8 0 0 1 16 0z"></path>
                                                    <path fill-rule="evenodd" d="M7.5 3a.5.5 0 0 1 .5.5v5.21l3.248 1.856a.5.5 0 0 1-.496.868l-3.5-2A.5.5 0 0 1 7 9V3.5a.5.5 0 0 1 .5-.5z"></path>
                                                </svg>
                                            </button>
                                        </div>

                                        <div class="ct-checklist-item__footer d-none">
                                            <div class="float-left mt-1">
                                                <div class="ct-task-option d-flex">
                                                    <div class="ct-task-assignee ct-option-btn d-flex">
                                                        <ul class="facepile-list"></ul>
                                                        <div class="dropdown">
                                                            <button class="btn btn-secondary dropdown-toggle ct-option-btn dropdownAssignment" type="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" style="padding: 4px 9px;">
                                                                <svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-person-plus" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                                                                    <path fill-rule="evenodd" d="M8 5a2 2 0 1 1-4 0 2 2 0 0 1 4 0zM6 8a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm6 5c0 1-1 1-1 1H1s-1 0-1-1 1-4 6-4 6 3 6 4zm-1-.004c-.001-.246-.154-.986-.832-1.664C9.516 10.68 8.289 10 6 10c-2.29 0-3.516.68-4.168 1.332-.678.678-.83 1.418-.832 1.664h10zM13.5 5a.5.5 0 0 1 .5.5V7h1.5a.5.5 0 0 1 0 1H14v1.5a.5.5 0 0 1-1 0V8h-1.5a.5.5 0 0 1 0-1H13V5.5a.5.5 0 0 1 .5-.5z"></path>
                                                                </svg>
                                                            </button>
                                                            <div class="dropdown-menu text-right" aria-labelledby="dropdownAssignment">
                                                                                        <h6 class="dropdown-header">
                                                                                                رئیس پروژه
                                                                                            </h6>
                                                                                        <div class="dropdown-item d-flex " type="button" data-value="None">
                                                                                                <img src="/media/Industry%20Profile/industry%40gmail.com/photo_2019-11-03_00-03-09.jpg" class="ml-1" alt="چمران تیم" width="32px">
                                                                                                <div class="mt-auto mb-auto">
                                                                                                    چمران تیم
                                                                                                    <span> (None@) </span>
                                                                                                </div>
                                                                                            </div>
                                                                                        <h6 class="dropdown-header">استاد</h6>
                                                                                        <div class="dropdown-item d-flex " type="button" data-value="sepehr">
                                                                                                    
                                                                                                        <img src="/media/Expert%20Profile/expert%40gmail.com/photo_2019-02-15_13-45-24.jpg" alt="سپهر متانت" class="ml-1" width="32px">
                                                                                                    
                                                                                                    <div class="mt-auto mb-auto">سپهر متانت<span> (sepehr@) </span>
                                                                                                    </div>
                                                                                                </div>
                                                                                        <h6 class="dropdown-header">پژوهشگر</h6>
                                                                                        <div class="dropdown-item d-flex selected" type="button" data-value="reza">
                                                                                                  <img src="/media/Researcher%20Profile/researcher%40gmail.com/smoke-hands-digital-art-abstract.jpg" alt="رضا باسره" class="ml-1" width="32px">
                                                                                                    <div class="mt-auto mb-auto">رضا باسره<span> (reza@) </span>
                                                                                                </div>
                                                                                        </div>
                                                                                        
                                                                                            <div class="dropdown-item d-flex " type="button" data-value="ahmad">
                                                                                                    
                                                                                                        <img src="/media/Researcher%20Profile/researcher1%40gmail.com/photo_2020-09-28_19-29-18.jpg" alt="هادی کاظمی" class="ml-1" width="32px">
                                                                                                    
                                                                                                    <div class="mt-auto mb-auto">هادی کاظمی<span> (ahmad@) </span>
                                                                                                    </div>
                                                                                                </div>
                                                                                        
                                                            </div>
                                                        </div>
                                                    </div>
                                                    <div class="ct-task-due ct-option-btn">
                                                        <button id="id_task_due${pk}" type="button" style="padding: 6px 10px;" dir="ltr">
                                                            <svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-clock" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                                                                <path fill-rule="evenodd" d="M8 15A7 7 0 1 0 8 1a7 7 0 0 0 0 14zm8-7A8 8 0 1 1 0 8a8 8 0 0 1 16 0z"></path>
                                                                <path fill-rule="evenodd" d="M7.5 3a.5.5 0 0 1 .5.5v5.21l3.248 1.856a.5.5 0 0 1-.496.868l-3.5-2A.5.5 0 0 1 7 9V3.5a.5.5 0 0 1 .5-.5z"></path>
                                                            </svg>
                                                            <span>${deadline}</span>
                                                        </button>
                                                    </div>
                                                </div>
                                            </div>
                                            <div class="">
                                                <button class="save-change btn btn-primary btn-sm" data-id="${pk}">
                                                    ذخیره
                                                </button>
                                                <button class="cancel-change btn btn-link text-dark btn-sm">
                                                    <svg width="2em" height="2em" viewBox="0 0 16 16" class="bi bi-x" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                                                        <path fill-rule="evenodd" d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708z">
                                                        </path>
                                                    </svg>
                                                </button>
                                            </div>
                                        </div>
                                    </div>
                                </div>`;
                    taskList.append(task);

                    // init new task options
                    init_task_options(taskList.find(".ct-checklist__item:last-child"));

                    // clear modal
                    addTaskForm.find("#id_task_title").html("");
                    addTaskForm.find(".tagId-list").html("");
                    addTaskForm.find(".ct-task-assignee.ct-option-btn .dropdown-item.selected").removeClass("selected");

                    // close modal and show success toast
                    $("#addTask").modal("hide");
                    iziToast.success({
                        rtl: true,
                        message: "تسک با موفقیت اضافه شد!",
                        position: 'bottomLeft'
                    });
                },
                error: function (data) {
                    iziToast.error({
                        rtl: true,
                        message: data,
                        position: 'bottomLeft'
                    });
                }
            });

        });
    }
    //****************************************//
    //  End Task Bar
    //****************************************//

});