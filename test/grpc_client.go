package main

import (
	"context"
	"log"
	"os"

	"github.com/flyteorg/flyte/flyteidl/gen/pb-go/flyteidl/admin"
	"github.com/flyteorg/flyte/flyteidl/gen/pb-go/flyteidl/core"
	"github.com/flyteorg/flyte/flyteidl/gen/pb-go/flyteidl/service"
	"google.golang.org/grpc"
)

const (
	domain         = "development"
	suffix         = "-1"
	workflowName   = "workflow" + suffix
	taskName       = "task" + suffix
	launchPlanName = "launch-plan" + suffix
	executionName  = "execution" + suffix
	command        = "sleep 1"
)

type DominoProjectInfoCtxKey struct{}

type DominoProjectInfo struct {
	ID string
}

func main() {
	ctx := context.Background()

	adminServiceAddress, ok := os.LookupEnv("FLYTE_PLATFORM_URL")
	if !ok {
		log.Fatalf("FLYTE_PLATFORM_URL environment variable not found")
	}

	// Connect to Flyte Admin service
	conn, err := grpc.Dial(adminServiceAddress, grpc.WithInsecure())
	if err != nil {
		log.Fatalf("Failed to connect to Flyte Admin service: %v", err)
	}
	defer conn.Close()

	// Create an AdminServiceClient
	client := service.NewAdminServiceClient(conn)

	// Add Domino project ID to context
	projectID, ok := os.LookupEnv("DOMINO_PROJECT_ID")
	if !ok {
		log.Fatalf("DOMINO_PROJECT_ID environment variable not found")
	}
	ctx = context.WithValue(ctx, DominoProjectInfoCtxKey{}, DominoProjectInfo{
		ID: projectID,
	})

	// Create a container task
	taskID := makeTaskID(projectID, taskName)
	createTask(ctx, client, taskID)

	// Create a workflow with the container task
	workflowID := makeWorkflowID(projectID, workflowName)
	createWorkflow(ctx, client, workflowID, taskID)

	// Create a launch plan
	launchPlanID := makeLaunchPlanID(projectID, launchPlanName)
	createLaunchPlan(ctx, client, workflowID, launchPlanID)

	// Create the execution
	createExecution(ctx, client, projectID, launchPlanID, executionName)
}

func makeTaskID(projectID string, name string) *core.Identifier {
	return &core.Identifier{
		ResourceType: core.ResourceType_TASK,
		Project:      projectID,
		Domain:       domain,
		Name:         name,
		Version:      "v1",
	}
}

func makeWorkflowID(projectID string, name string) *core.Identifier {
	return &core.Identifier{
		ResourceType: core.ResourceType_WORKFLOW,
		Project:      projectID,
		Domain:       domain,
		Name:         name,
		Version:      "v1",
	}
}

func makeLaunchPlanID(projectID string, name string) *core.Identifier {
	return &core.Identifier{
		ResourceType: core.ResourceType_LAUNCH_PLAN,
		Project:      projectID,
		Domain:       domain,
		Name:         name,
		Version:      "v1",
	}
}

func createTask(ctx context.Context, adminServiceClient service.AdminServiceClient, taskID *core.Identifier) {
	createTaskRequest := &admin.TaskCreateRequest{
		Id: taskID,
		Spec: &admin.TaskSpec{
			Template: &core.TaskTemplate{
				Id:   taskID,
				Type: "container",
				Metadata: &core.TaskMetadata{
					Runtime: &core.RuntimeMetadata{
						Type:    core.RuntimeMetadata_FLYTE_SDK,
						Version: "v0.0.0",
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
							command,
						},
					},
				},
			},
		},
	}
	_, err := adminServiceClient.CreateTask(ctx, createTaskRequest)
	if err != nil {
		log.Fatalf("Failed to create task: %v", err)
	}
	log.Printf("Created task: %v", taskID)
}

func createWorkflow(ctx context.Context, adminServiceClient service.AdminServiceClient, workflowID *core.Identifier, taskID *core.Identifier) {
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
	_, err := adminServiceClient.CreateWorkflow(ctx, createWorkflowRequest)
	if err != nil {
		log.Fatalf("Failed to create workflow: %v", err)
	}
	log.Printf("Created workflow: %v", workflowID)
}

func createLaunchPlan(ctx context.Context, adminServiceClient service.AdminServiceClient, workflowID *core.Identifier, launchPlanID *core.Identifier) {
	createLaunchPlanRequest := &admin.LaunchPlanCreateRequest{
		Id: launchPlanID,
		Spec: &admin.LaunchPlanSpec{
			WorkflowId: workflowID,
		},
	}
	_, err := adminServiceClient.CreateLaunchPlan(ctx, createLaunchPlanRequest)
	if err != nil {
		log.Fatalf("Failed to create launch plan: %v", err)
	}
	log.Printf("Created launch plan: %v", launchPlanID)
}

func createExecution(ctx context.Context, adminServiceClient service.AdminServiceClient, projectID string, launchPlanID *core.Identifier, name string) {
	createExecutionRequest := &admin.ExecutionCreateRequest{
		Project: projectID,
		Domain:  domain,
		Name:    name,
		Spec: &admin.ExecutionSpec{
			LaunchPlan: launchPlanID,
		},
		Inputs: &core.LiteralMap{},
	}
	_, err := adminServiceClient.CreateExecution(ctx, createExecutionRequest)
	if err != nil {
		log.Fatalf("Failed to create execution: %v", err)
	}
	log.Println("Execution created successfully")
}
