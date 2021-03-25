// // bootstrap filter dropdown
$(document).ready(function () {
  $(".dropdown-menu a.dropdown-toggle").on("click", function (e) {
    if (!$(this).next().hasClass("show")) {
      $(this)
        .parents(".dropdown-menu")
        .first()
        .find(".show")
        .removeClass("show");
    }
    var $subMenu = $(this).next(".dropdown-menu");
    $subMenu.toggleClass("show");

    $(this)
      .parents("li.nav-item.dropdown.show")
      .on("hidden.bs.dropdown", function (e) {
        $(".dropdown-submenu .show").removeClass("show");
      });

    return false;
  });
});

// user search
let timer = null;
delaySearch = () => {
  clearTimeout(timer);
  timer = setTimeout(userSearch, 1000);
};

userSearch = () => {
  // alert("does this work");
  let user = document.getElementById("searchUsers").value;
  fetch(`search_users/${user}`)
    .then((res) => {
      return res.json();
    })
    .then((result) => {
      console.log(result);
    });
  console.log(user);
};

filterByCat = (cat) => {
  let divsToHide = document.getElementsByClassName("item");
  let countDiv = document.querySelector(".results span");
  let count = 0;
  for (let i = 0; i < divsToHide.length; i++) {
    if (divsToHide[i].classList.contains(`${cat}Cat`)) {
      divsToHide[i].style.display = "block";
      count++;
    } else {
      divsToHide[i].style.display = "none";
    }
  }
  countDiv.innerHTML = `Filter Results: ${count}`;
  countDiv.style.visibility = "visible";
};

filterByStorage = (storage) => {
  let countDiv = document.querySelector(".results span");
  let count = 0;
  let divsToHide = document.getElementsByClassName("item");
  for (let i = 0; i < divsToHide.length; i++) {
    if (divsToHide[i].classList.contains(`${storage}Storage`)) {
      divsToHide[i].style.display = "block";
      count++;
    } else {
      divsToHide[i].style.display = "none";
    }
  }
  countDiv.innerHTML = `Filter Results: ${count}`;
  countDiv.style.visibility = "visible";
};

filterByLocation = (location) => {
  let countDiv = document.querySelector(".results span");
  let count = 0;
  let divsToHide = document.getElementsByClassName("item");
  for (let i = 0; i < divsToHide.length; i++) {
    if (divsToHide[i].classList.contains(`${location}Location`)) {
      divsToHide[i].style.display = "block";
      count++;
    } else {
      divsToHide[i].style.display = "none";
    }
  }
  countDiv.innerHTML = `Filter Results: ${count}`;
  countDiv.style.visibility = "visible";
};

editMode = (item_id) => {
  let edit = document.querySelector(`.editButton${item_id}`);
  let editDiv = document.querySelector(`.editZone${item_id}`);
  let saveButton = document.querySelector(`.editZone${item_id} input`);
  editDiv.style.display = "block";
  edit.style.display = "none";
  let selectedDiv = document.querySelector(`#item${item_id}`);
  let storageSpan = document.querySelector(`#item${item_id} span.Storage`)
    .innerHTML;
  let updateStorage = document.querySelector(`#item${item_id} span.Storage`);
  let updateLocation = document.querySelector(`#item${item_id} span.Location`);
  // console.log(updateStorage, updateLocation);
  let locationSpan = document.querySelector(`#item${item_id} span.Location`)
    .innerHTML;
  // console.log(storageSpan, locationSpan);
  // let storedIn =
  saveButton.addEventListener("click", function (e) {
    e.preventDefault();

    selectedDiv.classList.remove(`${storageSpan}Storage`);
    selectedDiv.classList.remove(`${locationSpan}Location`);
    let selectedValue = document.querySelector(`.editZone${item_id} select`)
      .value;
    selectedDiv.classList.add(`${selectedValue}Storage`);
    updateStorage.innerHTML = selectedValue;

    pStoredIn = document.querySelector(`#item${item_id} p.stored_in`);
    // console.log(pStoredIn);
    let test1 = document.querySelector(`.editZone${item_id} select`);

    pStoredIn.innerHTML = `Stored in ${
      test1.options[test1.selectedIndex].text
    }`;

    fetch(`update_location/${item_id}`, {
      method: "PUT",
      body: JSON.stringify({ stored_in: parseInt(selectedValue) }),
    })
      .then((res) => {
        return res.json();
      })
      .then((result) => {
        selectedDiv.classList.add(`${result.location}Location`);
        updateLocation.innerHTML = `${result.location}`;
      });
    editDiv.style.display = "none";
    edit.style.display = "block";
  });
};

cancel = (item_id) => {
  let edit = document.querySelector(`.editButton${item_id}`);
  let editDiv = document.querySelector(`.editZone${item_id}`);
  editDiv.style.display = "none";
  edit.style.display = "block";
};

resetFilter = () => {
  let countDiv = document.querySelector(".results span");
  let count = 0;
  let divsToHide = document.getElementsByClassName("item");
  for (let i = 0; i < divsToHide.length; i++) {
    divsToHide[i].style.display = "block";
  }
  countDiv.innerHTML = `Filter Results: ${count}`;
  countDiv.style.visibility = "hidden";
};

deleteItem = (itemId) => {
  let deleteDiv = document.querySelector(`#item${itemId}`);
  deleteDiv.style.display = "none";
  fetch(`delete_item/${itemId}`);
};

sendHouseholdRequest = (userId) => {
  let userLi = document.querySelector(`.user${userId} button`);
  userLi.disabled = true;
  userLi.innerHTML = "Request Sent";
  userLi.classList.remove("btn-outline-primary");
  userLi.classList.add("btn-outline-secondary");
  fetch(`send_household_request/${userId}`);
};
