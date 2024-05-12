package main

import (
	"context"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"
	"log"
	"time"

	"github.com/flyteorg/flyte/flyteidl/gen/pb-go/flyteidl/admin"
	"github.com/flyteorg/flyte/flyteidl/gen/pb-go/flyteidl/core"
	"github.com/flyteorg/flyte/flyteidl/gen/pb-go/flyteidl/service"
	"google.golang.org/grpc"
)

const (
	adminServiceAddress = "localhost:9089" // Assuming Flyte Admin service is running locally on port 8080
)

func main() {
	// Connect to Flyte Admin service
	conn, err := grpc.Dial(adminServiceAddress, grpc.WithInsecure())
	if err != nil {
		log.Fatalf("Failed to connect to Flyte Admin service: %v", err)
	}
	defer conn.Close()

	// Create an AdminServiceClient
	client := service.NewAdminServiceClient(conn)

	// Create and register a project
	projectID := "my-project"
	registerProject(client, projectID, "My project")

	// Create a container task
	taskID := makeTaskID(projectID, "task-1")
	createTask(client, taskID)

	// Create a workflow with the container task
	workflowID := makeWorkflowID(projectID, "workflow-1")
	createWorkflow(client, workflowID, taskID)

	taskID = makeTaskID(projectID, "task-2")
	createTask(client, taskID)

	workflowID = makeWorkflowID(projectID, "workflow-2")
	createWorkflow(client, workflowID, taskID)

	// Create a launch plan
	launchPlanID := makeLaunchPlanID(projectID, "launch-plan-2")
	createLaunchPlan(client, workflowID, launchPlanID)

	// Wait for a brief moment before creating the execution (optional)
	time.Sleep(5 * time.Second)

	// Create the execution
	createExecution(client, projectID, launchPlanID, "execution-1")
}

func makeTaskID(projectID string, name string) *core.Identifier {
	return &core.Identifier{
		ResourceType: core.ResourceType_TASK,
		Project:      projectID,
		Domain:       "development",
		Name:         name,
		Version:      "v1",
	}
}

func makeWorkflowID(projectID string, name string) *core.Identifier {
	return &core.Identifier{
		ResourceType: core.ResourceType_WORKFLOW,
		Project:      projectID,
		Domain:       "development",
		Name:         name,
		Version:      "v1",
	}
}

func makeLaunchPlanID(projectID string, name string) *core.Identifier {
	return &core.Identifier{
		ResourceType: core.ResourceType_LAUNCH_PLAN,
		Project:      projectID,
		Domain:       "development",
		Name:         name,
		Version:      "v1",
	}
}

func registerProject(adminServiceClient service.AdminServiceClient, projectID string, projectName string) {
	registerProjectRequest := &admin.ProjectRegisterRequest{
		Project: &admin.Project{
			Id:   projectID,
			Name: projectName,
		},
	}
	_, err := adminServiceClient.RegisterProject(context.Background(), registerProjectRequest)
	if err != nil {
		if status.Code(err) == codes.AlreadyExists {
			log.Println("Project already registered")
		} else {
			log.Fatalf("Failed to register project: %v", err)
		}
	} else {
		log.Printf("Registered project: %v", projectID)
	}
}

func createTask(adminServiceClient service.AdminServiceClient, taskID *core.Identifier) {
	containerTaskSpec := &admin.TaskSpec{
		Template: &core.TaskTemplate{
			Id:   taskID,
			Type: "container",
			Metadata: &core.TaskMetadata{
				Runtime: &core.RuntimeMetadata{
					Type:    core.RuntimeMetadata_FLYTE_SDK,
					Version: "v0.1.0",
				},
			},
			Interface: &core.TypedInterface{
				Inputs:  &core.VariableMap{},
				Outputs: &core.VariableMap{},
			},
			Target: &core.TaskTemplate_Container{
				Container: &core.Container{
					Image: "alpine",
					Command: []string{
						"sh",
						"-c",
					},
					Args: []string{
						"sleep 30",
					},
				},
			},
		},
	}
	createTaskRequest := &admin.TaskCreateRequest{
		Id:   taskID,
		Spec: containerTaskSpec,
	}
	_, err := adminServiceClient.CreateTask(context.Background(), createTaskRequest)
	if err != nil {
		log.Fatalf("Failed to create task: %v", err)
	}
	log.Printf("Created task: %v", taskID)
}

func createWorkflow(adminServiceClient service.AdminServiceClient, workflowID *core.Identifier, taskID *core.Identifier) {
	createWorkflowRequest := &admin.WorkflowCreateRequest{
		Id: workflowID,
		Spec: &admin.WorkflowSpec{
			Template: &core.WorkflowTemplate{
				Nodes: []*core.Node{
					{
						Id: "node-1",
						Target: &core.Node_TaskNode{
							TaskNode: &core.TaskNode{
								Reference: &core.TaskNode_ReferenceId{
									ReferenceId: taskID,
								},
							},
						},
					},
				},
			},
		},
	}
	_, err := adminServiceClient.CreateWorkflow(context.Background(), createWorkflowRequest)
	if err != nil {
		log.Fatalf("Failed to create workflow: %v", err)
	}
	log.Printf("Created workflow: %v", workflowID)
}

func createLaunchPlan(adminServiceClient service.AdminServiceClient, workflowID *core.Identifier, launchPlanID *core.Identifier) {
	createLaunchPlanRequest := &admin.LaunchPlanCreateRequest{
		Id: launchPlanID,
		Spec: &admin.LaunchPlanSpec{
			WorkflowId: workflowID,
			EntityMetadata: &admin.LaunchPlanMetadata{
				Schedule: &admin.Schedule{
					ScheduleExpression: &admin.Schedule_CronSchedule{
						CronSchedule: &admin.CronSchedule{
							Schedule: "* * * * *", // Execute every minute
						},
					},
				},
			},
		},
	}
	_, err := adminServiceClient.CreateLaunchPlan(context.Background(), createLaunchPlanRequest)
	if err != nil {
		log.Fatalf("Failed to create launch plan: %v", err)
	}
	log.Printf("Created launch plan: %v", launchPlanID)
}

func createExecution(adminServiceClient service.AdminServiceClient, projectID string, launchPlanID *core.Identifier, name string) {
	createExecutionRequest := &admin.ExecutionCreateRequest{
		Project: projectID,
		Domain:  "development",
		Name:    name,
		Spec: &admin.ExecutionSpec{
			LaunchPlan: launchPlanID,
			Metadata: &admin.ExecutionMetadata{
				Mode: admin.ExecutionMetadata_MANUAL,
			},
			NotificationOverrides: &admin.ExecutionSpec_DisableAll{
				DisableAll: true,
			},
		},
		Inputs: &core.LiteralMap{},
	}
	_, err := adminServiceClient.CreateExecution(context.Background(), createExecutionRequest)
	if err != nil {
		log.Fatalf("Failed to create execution: %v", err)
	}
	log.Println("Execution created successfully")
}
