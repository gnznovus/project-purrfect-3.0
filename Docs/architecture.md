# Purrfect Core Architecture

## Overview

Purrfect Core is responsible for orchestrating user requests through a controlled execution pipeline.

The current architecture separates:

- Request creation
- Execution orchestration
- Request handling
- Result processing
- State mutation

Each component has a single responsibility.

---

# Execution Flow

```text
User Input

    |
    v

ContextBuilder

    |
    v

RequestContext

    |
    v

CoreEngine

    |
    v

Router

    |
    v

Handler

    |
    v

CoreResult

    |
    +----------------+
    |                |
    v                v

Response        State Updates

                    |
                    v

          StateUpdateProcessor

                    |
                    v

        ConversationStateManager
```

---

# Components

## ContextBuilder

Responsibility:

Create a `RequestContext` from incoming user input and current conversation state.

It owns:

- request ID creation
- initial request metadata
- context creation

It does not:

- execute requests
- call handlers
- modify state

---

## RequestContext

Responsibility:

Carry the current execution information through the system.

Current data:

- request ID
- user input
- conversation state
- metadata

`ConversationState` stays inside `RequestContext` because it represents application execution state.

---

## CoreEngine

Responsibility:

Coordinate request execution.

CoreEngine decides:

- which handler receives control
- when confirmation handling takes priority
- when state updates should be processed
- how failures are converted into errors

CoreEngine does not:

- implement business logic
- modify state directly
- understand individual handler behavior

---

## Router

Responsibility:

Resolve the correct handler based on current conversation mode.

Current routing:

```text
ConversationMode
        |
        v
     Handler
```

---

## Handler

Responsibility:

Process a request and return a `CoreResult`.

Handlers do not:

- directly modify global state
- bypass CoreEngine
- control orchestration flow

Example:

```text
RequestContext

      |

Handler

      |

CoreResult
```

---

## CoreResult

Responsibility:

Provide a standard result contract between handlers and CoreEngine.

Contains:

- result type
- response content
- state updates
- metadata

---

## StateUpdateProcessor

Responsibility:

Apply requested state changes.

Flow:

```text
Handler

  |

CoreResult.state_updates

  |

StateUpdateProcessor

  |

ConversationStateManager
```

The processor exists as a boundary so future state update validation can be added without changing handlers.

---

## ConversationStateManager

Responsibility:

Own conversation state mutation.

It controls:

- mode changes
- active task changes
- pending transitions
- transition validation

Other components should not directly mutate conversation state.

---

# State Transition Flow

Example:

```text
Handler

"switch to planner"

        |

        v

REQUEST_MODE_CHANGE

        |

        v

ConversationStateManager

        |

        v

PendingTransition

        |

        v

ConfirmationHandler

        |

        +---- Accept
        |
        v

New Mode

        |

        +---- Reject
        |
        v

Clear Pending Transition
```

---

# Error Handling

Errors are converted at the CoreEngine boundary.

Flow:

```text
Handler Error

      |

      v

CoreEngine

      |

      v

CoreResult(
    type="error"
)
```

This prevents internal exceptions from leaking outside the execution pipeline.

---

# Testing Strategy

The project separates tests by responsibility.

## Unit Tests

Component behavior:

- ContextBuilder
- ConversationStateManager
- Handlers
- CoreEngine

## Pipeline Tests

Verify components work together:

```text
ContextBuilder

      |

CoreEngine

      |

Handler

      |

StateProcessor

      |

StateManager
```

---

# Current Design Principles

## Single Responsibility

Each component owns one responsibility.

## Controlled State Changes

State mutation happens through `ConversationStateManager`.

## Explicit Contracts

Communication happens through:

- RequestContext
- CoreResult
- StateUpdate
- LLMRequest
- LLMResponse

## Replaceable Components

Handlers and processors can evolve without rewriting CoreEngine.

## LLMService

Responsibility:

Coordinate all Large Language Model interactions.

It owns:

- building LLM requests
- calling providers
- returning structured responses

It does not:

- know which model implementation is used
- perform application orchestration
- modify conversation state

## LLMProvider

Responsibility:

Provide a provider-specific implementation for language model execution.

Current implementations:

- FakeLLMProvider
- OllamaProvider

Future providers may include:

- OpenAI
- Anthropic
- Local models

The provider returns a standardized `LLMResponse`.

## LLMRequest / LLMResponse

Responsibility:

Provide a stable contract between application logic and language model providers.

These models isolate provider-specific APIs from the rest of the system.

# Dependency Direction

Dependencies flow inward.

```
CoreEngine
    |
    v
Handler
    |
    v
LLMService
    |
    v
LLMProvider
```

Lower layers never depend on higher layers.

For example:

- CoreEngine does not know about Ollama.
- Handlers do not know provider implementations.
- Providers do not know CoreResult or ConversationState.

## Replaceable Implementations

Handlers, providers, and processors can be replaced without rewriting CoreEngine.

Examples:

- FakeLLMProvider ↔ OllamaProvider
- Future OpenAIProvider
- Different handler implementations