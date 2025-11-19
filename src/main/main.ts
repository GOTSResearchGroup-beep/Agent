/* eslint global-require: off, no-console: off, promise/always-return: off */

/**
 * This module executes inside of electron's main process. You can start
 * electron renderer process from here and communicate with the other processes
 * through IPC.
 *
 * When running `npm run build` or `npm run build:main`, this file is compiled to
 * `./src/main.js` using webpack. This gives us some performance wins.
 */
import { app, ipcMain } from 'electron';
import log from 'electron-log';
import { autoUpdater } from 'electron-updater';
import path from 'path';
import { mainZustandBridge } from 'zutron/main';
import { createMainWindow } from './window';
import { store } from './store/create';

class AppUpdater {
  constructor() {
    log.transports.file.level = 'info';
    autoUpdater.logger = log;
    // Disable auto-update in development to avoid version errors
    if (process.env.NODE_ENV === 'production') {
      autoUpdater.checkForUpdatesAndNotify();
    }
  }
}

ipcMain.on('ipc-example', async (event, arg) => {
  const msgTemplate = (pingPong: string) => `IPC test: ${pingPong}`;
  console.log(msgTemplate(arg));
  event.reply('ipc-example', msgTemplate('pong'));
});

if (process.env.NODE_ENV === 'production') {
  const sourceMapSupport = require('source-map-support');
  sourceMapSupport.install();
}

const isDebug =
  process.env.NODE_ENV === 'development' || process.env.DEBUG_PROD === 'true';

if (isDebug) {
  require('electron-debug')({ showDevTools: false });
}

const installExtensions = async () => {
  // Disable React DevTools installation to avoid Cr24 header errors
  // const installer = require('electron-devtools-installer');
  // const forceDownload = !!process.env.UPGRADE_EXTENSIONS;
  // const extensions = ['REACT_DEVELOPER_TOOLS'];
  // return installer
  //   .default(
  //     extensions.map((name) => installer[name]),
  //     forceDownload,
  //   )
  //   .catch(console.log);
  return Promise.resolve();
};

const initializeApp = async () => {
  if (isDebug) {
    await installExtensions();
  }

  const RESOURCES_PATH = app.isPackaged
    ? path.join(process.resourcesPath, 'assets')
    : path.join(__dirname, '../../assets');

  const getAssetPath = (...paths: string[]): string => {
    return path.join(RESOURCES_PATH, ...paths);
  };

  // Initialize the Zutron bridge BEFORE creating the window
  let unsubscribe: (() => void) | undefined;

  const mainWindow = await createMainWindow(getAssetPath);

  // Set up the bridge after window is created but before it loads content
  const bridgeResult = mainZustandBridge(ipcMain, store, [mainWindow], {
    // reducer: rootReducer,
  });
  unsubscribe = bridgeResult.unsubscribe;

  // Remove this if your app does not use auto updates
  // eslint-disable-next-line
  new AppUpdater();

  app.on('quit', () => {
    if (unsubscribe) unsubscribe();
  });
};

/**
 * Add event listeners...
 */

app.on('window-all-closed', () => {
  // Respect the OSX convention of having the application in memory even
  // after all windows have been closed
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app
  .whenReady()
  .then(async () => {
    await initializeApp();
  })
  .catch(console.log);
