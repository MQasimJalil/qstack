---- MODULE CancelRetry ----
EXTENDS Naturals

CONSTANT AcceptStaleCompletion
VARIABLES attempt, status, pending, event, previousStatus

vars == <<attempt, status, pending, event, previousStatus>>

Init ==
    /\ attempt = 1
    /\ status = "running"
    /\ pending = {1}
    /\ event = "start"
    /\ previousStatus = status

Cancel ==
    /\ attempt = 1
    /\ status = "running"
    /\ status' = "cancelled"
    /\ event' = "cancel"
    /\ previousStatus' = status
    /\ UNCHANGED <<attempt, pending>>

Retry ==
    /\ attempt = 1
    /\ status = "cancelled"
    /\ attempt' = 2
    /\ status' = "running"
    /\ pending' = pending \cup {2}
    /\ event' = "retry"
    /\ previousStatus' = status

DeliverRetry ==
    /\ 2 \in pending
    /\ status' = "succeeded"
    /\ pending' = pending \ {2}
    /\ event' = "deliver-retry"
    /\ previousStatus' = status
    /\ UNCHANGED attempt

DeliverOriginal ==
    /\ 1 \in pending
    /\ pending' = pending \ {1}
    /\ status' = IF (attempt = 1 /\ status = "running")
                   \/ (AcceptStaleCompletion /\ attempt = 2 /\ status = "succeeded")
                 THEN "failed" ELSE status
    /\ event' = "deliver-original"
    /\ previousStatus' = status
    /\ UNCHANGED attempt

Quiescent == /\ pending = {} /\ status # "cancelled" /\ UNCHANGED vars

Next == Cancel \/ Retry \/ DeliverRetry \/ DeliverOriginal \/ Quiescent
Spec == Init /\ [][Next]_vars

StaleCompletionCannotChangeStatus ==
    (attempt = 2 /\ event = "deliver-original") => status = previousStatus
====
