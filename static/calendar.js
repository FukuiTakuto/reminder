axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"
axios.defaults.xsrfCookieName = "csrftoken"

document.addEventListener('DOMContentLoaded', function () {

    var calendarEl = document.getElementById('calendar');

    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',

        selectable:true,
        select: function(info){
          //alert("selected"+info.startStr+"to"+info.endStr);

          const eventName = prompt("予定を入力してください");

          if(eventName){
            axios.post("/app/add/",{
              start_date : info.start.valueOf(),
              end_date : info.end.valueOf(),
              event_name : eventName,
            })
            .then(() => {
              calendar.addEvent({
              title:eventName,
              start:info.start,
              end:info.end,
              allDay:true,
              });
            })
            .catch(() => {
              alert("イベント登録に失敗");
            });
          }
        },
        events : function(info, successCallback, failureCallback){
          axios.
               post("/app/get/",{
                start_date : info.start.valueOf(),
                end_date : info.end.valueOf(),
              })
              .then((response) => {
                calendar.removeAllEvents();
                successCallback(response.data);
                console.log("受け取ったデータ:", response.data);
              })
              .catch(() => {
                alert("表示に失敗")
              });
        },
    });

    calendar.render();
});