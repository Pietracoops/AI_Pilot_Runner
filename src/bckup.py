


   for constraint in constraints:
        
        # Get Evaluation criteria
        constraint_eval = constraint.hasEvaluationCriteria


        # constraint could also be a list of tasks, if so we need to recursively call this function
        if len(constraint_eval) != 0 and constraint_eval[0].is_a[0] == onto_task.Task:
            task_validation, constraint_validation = get_task_validation(constraint_eval, current_data_list, task_validation,constraint_validation, onto_task)
            task_validation[task.name] = True # Initially set to true
            for constraint_task in constraint_eval:
                if task_validation[constraint_task.name] == False: # If any of the tasks are False, return False
                    task_validation[task.name] = False
                    break
            continue

        constraint_eval_name = constraint_eval[0].name
        # Check if constrain already in constraint_validation
        if constraint_eval_name in constraint_validation:
            constraint_validation_tmp[constraint_eval_name] = constraint_validation[constraint_eval_name]
            continue

        if constraint_eval_name == '10085':
            print("here")

        # Get CAE Value from data slice
        error_code, cae_value = cae_log_utils.get_cae_val_from_data(constraint_eval_name, current_data_list)
        if error_code == 1:
            constraint_validation_tmp[constraint_eval_name] = True
            continue
        elif error_code == 2:
            print(f"Error occured in get_cae_val_from_data cae_label for {constraint_eval_name} "
                    f"was not found in databases")

        # Chek constraint validation
        error_code, constraint_validation_tmp = check_constraint_valid(constraint, constraint_validation_tmp, cae_value)
        if error_code == 1:
            print(f"Error in check_constraint_valid with constraint {constraint.name}")
            constraint_validation_tmp[constraint_eval_name] = False
            continue