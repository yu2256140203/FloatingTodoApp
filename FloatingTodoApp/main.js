const { app, BrowserWindow, ipcMain, Notification, Tray, Menu, screen } = require('electron');
const path = require('path');

let mainWindow;
let tray;

function createWindow() {
  const { width, height } = screen.getPrimaryDisplay().workAreaSize;

  mainWindow = new BrowserWindow({
    width: 320,
    height: 500,
    x: width - 340,
    y: Math.floor(height / 2) - 250,
    frame: false,
    transparent: true,
    alwaysOnTop: true,
    resizable: false,
    skipTaskbar: true,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false
    }
  });

  mainWindow.loadFile('index.html');
  mainWindow.setAlwaysOnTop(true, 'screen-saver');
}

function createTray() {
  tray = new Tray(path.join(__dirname, 'icon.png'));
  const contextMenu = Menu.buildFromTemplate([
    { label: '显示', click: () => mainWindow.show() },
    { label: '退出', click: () => app.quit() }
  ]);
  tray.setToolTip('Floating ToDo');
  tray.setContextMenu(contextMenu);
}

app.whenReady().then(() => {
  createWindow();
  createTray();
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

// 处理提醒通知
ipcMain.on('show-notification', (event, { title, body }) => {
  new Notification({ title, body }).show();
});

// 处理窗口拖动
ipcMain.on('window-drag', (event, { x, y }) => {
  mainWindow.setPosition(x, y);
});

// 处理窗口最小化
ipcMain.on('window-minimize', () => {
  mainWindow.minimize();
});

// 处理窗口关闭
ipcMain.on('window-close', () => {
  mainWindow.close();
});
