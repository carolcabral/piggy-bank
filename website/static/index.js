function deleteNote(noteId) {
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ noteId }),
  }).then((res) => {
    window.location.href = "/";
  });
}

function nextMonth(currentMonth, currentYear) {
  fetch("/", {
    method: "POST",
    body: JSON.stringify({ currentMonth, currentYear }),
  }).then((res) => {
    //window.location.href = "/";
  });
}
