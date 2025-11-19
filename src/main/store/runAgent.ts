import {
  BetaMessage,
  BetaMessageParam,
} from '@anthropic-ai/sdk/resources/beta/messages/messages';
import { Button, Key, keyboard, mouse, Point } from '@nut-tree-fork/nut-js';
// import { createCanvas, loadImage } from 'canvas';
import { desktopCapturer, screen } from 'electron';
import { anthropic, createAnthropicClient } from './anthropic';
import { AppState, NextAction } from './types';
import { extractAction } from './extractAction';
import { hideWindowBlock, showWindow } from '../window';

const MAX_STEPS = 50;

function getScreenDimensions(): { width: number; height: number } {
  const primaryDisplay = screen.getPrimaryDisplay();
  return primaryDisplay.size;
}

function getAiScaledScreenDimensions(): { width: number; height: number } {
  const { width, height } = getScreenDimensions();
  const aspectRatio = width / height;

  let scaledWidth: number;
  let scaledHeight: number;

  if (aspectRatio > 1280 / 800) {
    // Width is the limiting factor
    scaledWidth = 1280;
    scaledHeight = Math.round(1280 / aspectRatio);
  } else {
    // Height is the limiting factor
    scaledHeight = 800;
    scaledWidth = Math.round(800 * aspectRatio);
  }

  return { width: scaledWidth, height: scaledHeight };
}

const getScreenshot = async (): Promise<string> => {
  const primaryDisplay = screen.getPrimaryDisplay();
  const { width, height } = primaryDisplay.size;
  const aiDimensions = getAiScaledScreenDimensions();

  return hideWindowBlock(async () => {
    const sources = await desktopCapturer.getSources({
      types: ['screen'],
      thumbnailSize: { width, height },
    });
    const primarySource = sources[0]; // Assuming the first source is the primary display

    if (primarySource) {
      const screenshot = primarySource.thumbnail;
      // Resize the screenshot to AI dimensions
      const resizedScreenshot = screenshot.resize(aiDimensions);
      // Convert the resized screenshot to a base64-encoded PNG
      const base64Image = resizedScreenshot.toPNG().toString('base64');
      return base64Image;
    }
    throw new Error('No display found for screenshot');
  });
};

const mapToAiSpace = (x: number, y: number) => {
  const { width, height } = getScreenDimensions();
  const aiDimensions = getAiScaledScreenDimensions();
  return {
    x: (x * aiDimensions.width) / width,
    y: (y * aiDimensions.height) / height,
  };
};

const mapFromAiSpace = (x: number, y: number) => {
  const { width, height } = getScreenDimensions();
  const aiDimensions = getAiScaledScreenDimensions();
  return {
    x: (x * width) / aiDimensions.width,
    y: (y * height) / aiDimensions.height,
  };
};

const promptForAction = async (
  runHistory: BetaMessageParam[],
  get: () => AppState,
  set: (state: Partial<AppState>) => void,
): Promise<BetaMessageParam> => {
  // Strip images from all but the last message
  const historyWithoutImages = runHistory.map((msg, index) => {
    if (index === runHistory.length - 1) return msg; // Keep the last message intact
    if (Array.isArray(msg.content)) {
      return {
        ...msg,
        content: msg.content.map((item) => {
          if (item.type === 'tool_result' && typeof item.content !== 'string') {
            return {
              ...item,
              content: item.content?.filter((c) => c.type !== 'image'),
            };
          }
          return item;
        }),
      };
    }
    return msg;
  });

  const apiKey = get().apiKey || process.env.ANTHROPIC_API_KEY;
  if (!apiKey) {
    set({ error: 'API key not found. Please set your Anthropic API key.', running: false });
    return;
  }
  
  const client = createAnthropicClient(apiKey);

  const message = await client.beta.messages.create({
    model: 'claude-3-7-sonnet-20250219',
    max_tokens: 1024,
    tools: [
      {
        type: 'computer_20250124',
        name: 'computer',
        display_width_px: getAiScaledScreenDimensions().width,
        display_height_px: getAiScaledScreenDimensions().height,
        display_number: 1,
      },
      {
        name: 'finish_run',
        description:
          'Call this function when you have achieved the goal of the task.',
        input_schema: {
          type: 'object',
          properties: {
            success: {
              type: 'boolean',
              description: 'Whether the task was successful',
            },
            error: {
              type: 'string',
              description: 'The error message if the task was not successful',
            },
          },
          required: ['success'],
        },
      },
    ],
    system: `You are controlling a Windows computer in Spanish. The user will ask you to perform a task and you should use their computer to do so. After each step, take a screenshot and carefully evaluate if you have achieved the right outcome. Explicitly show your thinking: "I have evaluated step X..." If not correct, try again. Only when you confirm a step was executed correctly should you move on to the next one.

CRITICAL: For ALL click actions (left_click, right_click, double_click), you MUST specify the exact coordinate [x, y] where to click. Look at the screenshot, identify the exact pixel location of the element you want to click, and include that coordinate in your action. Never click without coordinates.

Examples:
- To click on an icon at position x=100, y=150: use coordinate [100, 150]
- To double-click on a file: identify its location and use coordinate [x, y]

Remember: The system is in Spanish, so applications like "Notepad" are called "Bloc de notas". You should always call a tool! Always return a tool call. Remember call the finish_run tool when you have achieved the goal of the task.`,
    // tool_choice: { type: 'any' },
    messages: historyWithoutImages,
    betas: ['computer-use-2025-01-24'],
  });

  return { content: message.content, role: message.role };
};

export const performAction = async (action: NextAction) => {
  console.log('PERFORMING ACTION:', action);
  switch (action.type) {
    case 'mouse_move':
      const { x, y } = mapFromAiSpace(action.x, action.y);
      console.log('Moving mouse to:', { x, y });
      await mouse.setPosition(new Point(x, y));
      break;
    case 'left_click_drag':
      const { x: dragX, y: dragY } = mapFromAiSpace(action.x, action.y);
      const currentPosition = await mouse.getPosition();
      console.log('Dragging from', currentPosition, 'to', { x: dragX, y: dragY });
      await mouse.drag([currentPosition, new Point(dragX, dragY)]);
      break;
    case 'cursor_position':
      const position = await mouse.getPosition();
      const aiPosition = mapToAiSpace(position.x, position.y);
      console.log('Current mouse position:', position, 'AI space:', aiPosition);
      // TODO: actually return the position
      break;
    case 'left_click':
      console.log('Performing left click');
      if (action.x && action.y) {
        const { x: clickX, y: clickY } = mapFromAiSpace(action.x, action.y);
        console.log('Moving to coordinates:', { x: clickX, y: clickY });
        await mouse.setPosition(new Point(clickX, clickY));
        await new Promise(resolve => setTimeout(resolve, 100));
      }
      await mouse.leftClick();
      break;
    case 'right_click':
      if (action.x && action.y) {
        const { x: clickX, y: clickY } = mapFromAiSpace(action.x, action.y);
        console.log('Performing right click at:', { x: clickX, y: clickY });
        await mouse.setPosition(new Point(clickX, clickY));
        await new Promise(resolve => setTimeout(resolve, 100));
      } else {
        console.log('Performing right click at current position');
      }
      await mouse.rightClick();
      break;
    case 'middle_click':
      if (action.x && action.y) {
        const { x: clickX, y: clickY } = mapFromAiSpace(action.x, action.y);
        console.log('Performing middle click at:', { x: clickX, y: clickY });
        await mouse.setPosition(new Point(clickX, clickY));
        await new Promise(resolve => setTimeout(resolve, 100));
      } else {
        console.log('Performing middle click at current position');
      }
      await mouse.click(Button.MIDDLE);
      break;
    case 'double_click':
      console.log('Performing double click');
      if (action.x && action.y) {
        const { x: clickX, y: clickY } = mapFromAiSpace(action.x, action.y);
        console.log('Moving to coordinates:', { x: clickX, y: clickY });
        await mouse.setPosition(new Point(clickX, clickY));
        await new Promise(resolve => setTimeout(resolve, 100));
      }
      await mouse.doubleClick(Button.LEFT);
      break;
    case 'type':
      console.log('Typing text:', action.text);
      // Set typing delay to 0ms for instant typing
      keyboard.config.autoDelayMs = 0;
      await keyboard.type(action.text);
      // Reset delay back to default if needed
      keyboard.config.autoDelayMs = 500;
      break;
    case 'key':
      const keyMap = {
        Return: Key.Enter,
      };
      const keys = action.text.split('+').map((key) => {
        const mappedKey = keyMap[key as keyof typeof keyMap];
        if (!mappedKey) {
          throw new Error(`Tried to press unknown key: ${key}`);
        }
        return mappedKey;
      });
      await keyboard.pressKey(...keys);
      break;
    case 'screenshot':
      // Don't do anything since we always take a screenshot after each step
      break;
    default:
      throw new Error(`Unsupported action: ${action.type}`);
  }
};

export const runAgent = async (
  setState: (state: AppState) => void,
  getState: () => AppState,
) => {
  setState({
    ...getState(),
    running: true,
    runHistory: [{ role: 'user', content: getState().instructions ?? '' }],
    error: null,
  });

  while (getState().running) {
    // Add this check at the start of the loop
    if (getState().runHistory.length >= MAX_STEPS * 2) {
      setState({
        ...getState(),
        error: 'Maximum steps exceeded',
        running: false,
      });
      break;
    }

    try {
      const message = await promptForAction(getState().runHistory, getState, setState);
      setState({
        ...getState(),
        runHistory: [...getState().runHistory, message],
      });
      const { action, reasoning, toolId } = extractAction(
        message as BetaMessage,
      );
      console.log('REASONING', reasoning);
      console.log('ACTION', action);

      if (action.type === 'error') {
        setState({
          ...getState(),
          error: action.message,
          running: false,
        });
        break;
      } else if (action.type === 'finish') {
        setState({
          ...getState(),
          running: false,
        });
        break;
      }
      if (!getState().running) {
        break;
      }

      console.log('About to perform action:', action);
      await hideWindowBlock(async () => {
        console.log('Inside hideWindowBlock, performing action:', action);
        return await performAction(action);
      });

      await new Promise((resolve) => setTimeout(resolve, 500));
      if (!getState().running) {
        break;
      }

      setState({
        ...getState(),
        runHistory: [
          ...getState().runHistory,
          {
            role: 'user',
            content: [
              {
                type: 'tool_result',
                tool_use_id: toolId,
                content: [
                  {
                    type: 'text',
                    text: 'Here is a screenshot after the action was executed',
                  },
                  {
                    type: 'image',
                    source: {
                      type: 'base64',
                      media_type: 'image/png',
                      data: await getScreenshot(),
                    },
                  },
                ],
              },
            ],
          },
        ],
      });
    } catch (error: unknown) {
      setState({
        ...getState(),
        error:
          error instanceof Error ? error.message : 'An unknown error occurred',
        running: false,
      });
      break;
    }
  }
};
