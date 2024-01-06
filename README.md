## Folder Structure

### Folder Structure Before Running Scripts

- **Before running the scripts, the folder structure looks like:**

![Screenshot from 2024-01-06 11-20-13](https://github.com/ishtiaqSamdani/fetch-aws-resources/assets/82057297/abd2f509-317e-4ff0-b645-56791725f565)


### Running `index.py`

- When executing the following commands:

  ```bash
  cd <complete path>/python # or cd python
  python3 -u index.py
  ```

  It creates a new folder named `python_output`. Inside this folder, information about various AWS resources will be stored in individual JSON files such as `ec2.json`, `eks.json`, etc.

  ![Screenshot from 2024-01-06 11-29-11](https://github.com/ishtiaqSamdani/fetch-aws-resources/assets/82057297/5fb53110-198e-47f0-9376-4b8a60b54eaf)


## Optional: Excel (XLSX) File Generation

- The following steps are optional and involve running conversion scripts in the `python` folder to convert JSON files to Excel (XLSX) format.

### Creation of `python_excel`

- After running the conversion scripts, a new folder named `python_excel` is created. This folder contains Excel files converted from the previously generated JSON files.
```bash
  cd <complete path>/python # or cd python
  python3 -u conversion-cloudfront.py
  python3 -u conversion-ec2.py
  python3 -u conversion-ecr.py
  python3 -u conversion-ecs.py
  python3 -u conversion-eks.py
  python3 -u conversion-elasticip.py
  python3 -u conversion-loadbalancer.py
  python3 -u conversion-rds.py
```
  ![Screenshot from 2024-01-06 11-40-31](https://github.com/ishtiaqSamdani/fetch-aws-resources/assets/82057297/13143dc2-9558-42e2-a981-1b10df9cbca8)

## Automating Folder Creation with `script_to_automate.sh`

### Bash Script: `script_to_automate.sh`

### Running the Script

- To execute the script and automate the folder creation process, use the following commands:
  - give executable permissions to script_to_automate.sh file
    ```bash
    chmod +x script_to_automate.sh
    ```
  - run the script
    ```bash
    bash script_to_automate.sh # or ./script_to_automate.sh
    ```
  ![Screenshot from 2024-01-06 11-55-09](https://github.com/ishtiaqSamdani/fetch-aws-resources/assets/82057297/fb847392-578f-4bbf-8452-cb0ff761c217)

- The script changes to the specified directory, runs the main Python script (`index.py`), and then iterates through the conversion scripts to create both the `python_output` and `python_excel` folders.

  ![Screenshot from 2024-01-06 11-58-40](https://github.com/ishtiaqSamdani/fetch-aws-resources/assets/82057297/1636bf71-5943-4700-abdd-35e8a7286429)


## Automating with Cron Job

### Adding Cron Job

To automate the folder creation process regularly, you can set up a cron job. Use the following command to edit the crontab:

```bash
crontab -e
```
![Screenshot from 2024-01-06 12-18-48](https://github.com/ishtiaqSamdani/fetch-aws-resources/assets/82057297/0d987a8e-8881-4313-a17b-72048f7c0abc)


Then add the following line to execute the `script_to_automate.sh` script every day at 04:00 AM:

**press `I` for `INSERT MODE` to edit crontab interface**
 
```cron
4 0 * * * <complete path to folder>/script_to_automate.sh
```

For example:

```cron
4 0 * * * /home/ishts/Desktop/Projects/aws-data-scrap/script_to_automate.sh
```
This cron job runs the script daily at 04:00 AM, ensuring that your AWS resource information is updated regularly.

![Screenshot from 2024-01-06 12-19-03](https://github.com/ishtiaqSamdani/fetch-aws-resources/assets/82057297/20b3e72f-5d53-4449-8b87-4569cc2cf84e)

**press `:wq` to save and exit crontab interface**

### Verify Cron Job

After adding the cron job, you can check the list of existing cron jobs using the following command:

```bash
crontab -l
```
This will display the current cron job configurations.

![Screenshot from 2024-01-06 12-22-15](https://github.com/ishtiaqSamdani/fetch-aws-resources/assets/82057297/5c79aa05-1308-4a7f-b4e4-ac19a942769f)

### Logging (optional)

Consider redirecting the output of the cron job to a log file for troubleshooting purposes. Update the crontab entry as follows:

```cron
4 0 * * * <complete path to folder>/script_to_automate.sh >> <complete path to folder>/cron_log.txt 2>&1
```

For example:

```cron
4 0 * * * /home/ishts/Desktop/Projects/aws-data-scrap/script_to_automate.sh >> /home/ishts/Desktop/Projects/aws-data-scrap/cron_log.txt 2>&1
```

This will append both standard output and standard error to the specified log file.
## ADDITIONAL 

to genarate cronjob use : https://crontab-generator.org/





