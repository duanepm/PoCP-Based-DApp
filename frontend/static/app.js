let startTime, timerInterval;
let submittedMiners = new Set();
let registeredMiners = [];
let totalMiners = 0;
let timerRunning = false;

function formatTime(ms) {
  const date = new Date(ms);
  return date.toISOString().substr(14, 9); 
}

function startTimer() {
  startTime = performance.now();
  submittedMiners.clear();
  const display = document.getElementById('timerDisplay');
  const progressBar = document.getElementById('timerProgress');

  const maxTime = 10000;

  if (!timerRunning) {
    timerRunning = true;
    timerInterval = setInterval(() => {
      const elapsed = performance.now() - startTime;
      display.textContent = "⏱️ " + formatTime(elapsed);

      let progress = Math.min((elapsed / maxTime) * 100, 100);
      progressBar.style.width = `${progress}%`;
      progressBar.setAttribute("aria-valuenow", progress.toFixed(0));

      if (progress < 50) {
        progressBar.classList.remove("bg-warning", "bg-danger");
        progressBar.classList.add("bg-success");
      } else if (progress < 80) {
        progressBar.classList.remove("bg-success", "bg-danger");
        progressBar.classList.add("bg-warning");
      } else {
        progressBar.classList.remove("bg-success", "bg-warning");
        progressBar.classList.add("bg-danger");
      }
    }, 50);
  }
}

function stopTimer() {
  clearInterval(timerInterval);
  timerRunning = false;

  const progressBar = document.getElementById('timerProgress');
  progressBar.style.width = "0%";
  progressBar.setAttribute("aria-valuenow", "0");
  progressBar.classList.remove("bg-success", "bg-warning", "bg-danger");
}

async function loadMiners() {
  const res = await fetch('/miners');
  const data = await res.json();
  const select = document.getElementById('selectedMiner');
  select.innerHTML = '';

  registeredMiners = data.miners || []; // ✅ save globally
  registeredMiners.forEach(miner => {
    const option = document.createElement('option');
    option.value = miner;
    option.textContent = miner;
    select.appendChild(option);
  });
  totalMiners = registeredMiners.length;
}

async function updateLeaderboard() {
  const res = await fetch('/leaderboard');
  const data = await res.json();
  const tbody = document.getElementById('leaderboardTable');
  tbody.innerHTML = '';
  data.entries.forEach(entry => {
    const row = document.createElement('tr');
    row.innerHTML = `
      <td>${entry.miner}</td>
      <td>${entry.time.toFixed(3)}</td>
      <td>${entry.cp.toFixed(3)}</td>
    `;
    tbody.appendChild(row);
  });
}

async function updateRewards() {
    const tbody = document.getElementById('rewardsTable');
    tbody.innerHTML = '';
  
    try {
      const response = await fetch('/get_reward');
      const data = await response.json();
  
      const rewardMap = {};
      data.rewards.forEach(entry => {
        rewardMap[entry.address.toLowerCase()] = entry.reward;
      });
  
      for (const miner of registeredMiners) {
        const reward = rewardMap[miner.toLowerCase()] ?? 0;
  
        const row = document.createElement('tr');
        row.innerHTML = `
          <td>${miner}</td>
          <td>${reward}</td>
        `;
        tbody.appendChild(row);
      }
    } catch (err) {
      console.error("Failed to load rewards:", err);
    }
}

document.getElementById('registerForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const address = document.getElementById('hardhatAddressDropdown').value;
  if (!address) return;

  await fetch('/register', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ address })
  });

  await loadMiners();
  await updateRewards();
});


document.getElementById('miningForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const address = document.getElementById('selectedMiner').value;
  
    if (submittedMiners.has(address)) {
      alert("This miner has already submitted.");
      return;
    }
  
    const elapsed = performance.now() - startTime;
    const timeInSeconds = elapsed / 1000;
  
    const response = await fetch('/submit_time', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ address, time: timeInSeconds })
    });
  
    if (response.ok) {
      submittedMiners.add(address);
  
      // Immediately update leaderboard and rewards
      await updateLeaderboard();
      await updateRewards();
  
      if (submittedMiners.size === totalMiners) {
        stopTimer();
        alert("✅ All miners have submitted. Timer stopped.");
  
        // Ensure final state is rendered right after alert
        await updateLeaderboard();
        await updateRewards();
      }
    }
  });
  
  

document.getElementById('validatorForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const res = await fetch('/select_validator');
  const data = await res.json();
  document.getElementById('validatorResult').textContent = "Validator: " + data.validator;

  await updateRewards(); // Update rewards after validator is selected
});

document.getElementById('startMiningForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    await fetch('/reset_round', {
      method: 'POST',
    });
    submittedMiners.clear();
    await updateLeaderboard();
    await updateRewards();
  });


async function loadHardhatAddresses() {
  const res = await fetch('/hardhat_addresses');
  const data = await res.json();

  const dropdown = document.getElementById('hardhatAddressDropdown');
  dropdown.innerHTML = '';

  data.addresses.forEach(addr => {
    const option = document.createElement('option');
    option.value = addr;
    option.textContent = addr;
    dropdown.appendChild(option);
  });
}

  
window.onload = async () => {
  await loadMiners();
  await updateLeaderboard();
  await updateRewards();
  await loadHardhatAddresses();
};
