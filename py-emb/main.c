/*
 * main.c
 *
 * Full FreeRTOS queue send/receive example for x86
 * using FreeRTOS POSIX/Linux style port.
 *
 * Demonstrates:
 *   - Queue creation
 *   - Sender task
 *   - Receiver task
 *   - Scheduler start
 *
 * Author: OpenAI
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include "FreeRTOS.h"
#include "task.h"
#include "queue.h"

/*-----------------------------------------------------------
 * Application definitions
 *----------------------------------------------------------*/

/* Queue length: number of items queue can store */
#define APP_QUEUE_LENGTH         (5U)

/* Task stack sizes */
#define APP_SENDER_STACK_SIZE    (configMINIMAL_STACK_SIZE * 2)
#define APP_RECEIVER_STACK_SIZE  (configMINIMAL_STACK_SIZE * 2)

/* Task priorities */
#define APP_SENDER_PRIORITY      (tskIDLE_PRIORITY + 2)
#define APP_RECEIVER_PRIORITY    (tskIDLE_PRIORITY + 2)

/*-----------------------------------------------------------
 * Message structure
 *----------------------------------------------------------*/
typedef struct
{
    int id;
    char text[64];
} app_msg_t;

/* Queue handle */
static QueueHandle_t g_msg_queue = NULL;

/*-----------------------------------------------------------
 * Sender task
 *----------------------------------------------------------*/
static void sender_task(void *pvParameters)
{
    app_msg_t msg;
    int counter = 0;
    BaseType_t status;

    (void)pvParameters;

    memset(&msg, 0, sizeof(msg));

    while (1)
    {
        counter++;

        msg.id = counter;
        snprintf(msg.text, sizeof(msg.text), "Message from sender: %d", counter);

        status = xQueueSend(g_msg_queue, &msg, pdMS_TO_TICKS(100));

        if (status == pdPASS)
        {
            printf("[SENDER ] Sent -> id=%d, text=\"%s\"\n", msg.id, msg.text);
        }
        else
        {
            printf("[SENDER ] Queue full, failed to send id=%d\n", msg.id);
        }

        /* Send every 1 second */
        vTaskDelay(pdMS_TO_TICKS(1000));
    }
}

/*-----------------------------------------------------------
 * Receiver task
 *----------------------------------------------------------*/
static void receiver_task(void *pvParameters)
{
    app_msg_t msg;
    BaseType_t status;

    (void)pvParameters;

    memset(&msg, 0, sizeof(msg));

    while (1)
    {
        /*
         * Wait forever until one item becomes available.
         * This is typical consumer-task behavior.
         */
        status = xQueueReceive(g_msg_queue, &msg, portMAX_DELAY);

        if (status == pdPASS)
        {
            printf("[RECEIVER] Received <- id=%d, text=\"%s\"\n", msg.id, msg.text);
        }
        else
        {
            printf("[RECEIVER] Receive failed\n");
        }
    }
}

/*-----------------------------------------------------------
 * Hook functions
 *----------------------------------------------------------*/

/*
 * Called if a task overflows its stack.
 * For demo purposes we print and abort.
 */
void vApplicationStackOverflowHook(TaskHandle_t xTask, char *pcTaskName)
{
    (void)xTask;

    fprintf(stderr, "\n[ERROR] Stack overflow in task: %s\n",
            (pcTaskName != NULL) ? pcTaskName : "unknown");
    abort();
}

/*
 * Called if malloc fails inside FreeRTOS heap usage.
 */
void vApplicationMallocFailedHook(void)
{
    fprintf(stderr, "\n[ERROR] FreeRTOS malloc failed\n");
    abort();
}

/*
 * Optional idle hook.
 */
void vApplicationIdleHook(void)
{
    /* Keep empty for this example */
}

/*
 * Optional tick hook.
 */
void vApplicationTickHook(void)
{
    /* Keep empty for this example */
}

/*-----------------------------------------------------------
 * main
 *----------------------------------------------------------*/
int main(void)
{
    BaseType_t status;

    printf("========================================\n");
    printf(" FreeRTOS Queue Send/Receive Demo (x86)\n");
    printf("========================================\n");

    /* Create a queue that can hold APP_QUEUE_LENGTH app_msg_t objects */
    g_msg_queue = xQueueCreate(APP_QUEUE_LENGTH, sizeof(app_msg_t));
    if (g_msg_queue == NULL)
    {
        fprintf(stderr, "[MAIN   ] Queue creation failed\n");
        return EXIT_FAILURE;
    }

    printf("[MAIN   ] Queue created successfully\n");

    /* Create sender task */
    status = xTaskCreate(sender_task,
                         "sender_task",
                         APP_SENDER_STACK_SIZE,
                         NULL,
                         APP_SENDER_PRIORITY,
                         NULL);
    if (status != pdPASS)
    {
        fprintf(stderr, "[MAIN   ] sender_task creation failed\n");
        return EXIT_FAILURE;
    }

    printf("[MAIN   ] sender_task created\n");

    /* Create receiver task */
    status = xTaskCreate(receiver_task,
                         "receiver_task",
                         APP_RECEIVER_STACK_SIZE,
                         NULL,
                         APP_RECEIVER_PRIORITY,
                         NULL);
    if (status != pdPASS)
    {
        fprintf(stderr, "[MAIN   ] receiver_task creation failed\n");
        return EXIT_FAILURE;
    }

    printf("[MAIN   ] receiver_task created\n");

    printf("[MAIN   ] Starting scheduler...\n");

    /* Start FreeRTOS scheduler */
    vTaskStartScheduler();

    /*
     * Normally execution should never come here.
     * If it does, scheduler could not start.
     */
    fprintf(stderr, "[MAIN   ] Scheduler exited unexpectedly\n");
    return EXIT_FAILURE;
}