# AWS IAM

We are going to enable a minimum viable IAM setup for development. 

## Scenario
You’re a solo developer, using AWS for personal or prototype projects, but you want:
- To never use the root user except for account-level tasks.
- To have named IAM users/roles with principle of least privilege.
- To separate dev/automation roles from interactive human access.
- To use MFA and optionally short-lived CLI creds (via AWS SSO or aws sts assume-role).

### 1. Secure the Root Account

Do this once and never use it again.
- Enable MFA (use an authenticator app, not SMS).
- Add a billing contact email and alternate contact.
- Create a strong unique password (store in a password manager).
- Disable or rotate any access keys (root should have none).

### 2. Create an IAM Admin User or Role
You need a human user that can do everything except root-only billing tasks.

Option A (simpler): Create an “Admin” IAM user
- Go to IAM → Users → Create User
- Name: <name>-admin (or any name you want - just make it easy to remember and identify)
- Access type: AWS Management Console access
- Attach policy: AdministratorAccess
- Enable MFA for this user.
- Create a group called admins and attach AdministratorAccess --> then add yourself to that group.
- Create an Access Key for CLI use (optional; or see step 4 for better practice).

Option B (modern best practice): Use IAM Identity Center (AWS SSO)
- Go to AWS IAM Identity Center (SSO) and enable it.
- Create a user “Andy McMahon”.
- Assign that user to a permission set = AdministratorAccess.
- You’ll log in via aws sso login, and the CLI will handle temporary creds.
✅ This is the cleanest pattern, no access keys stored.

We will go with option B.
Enable IAM Identity Center for a region near you
1. Go to Users → Add user
2. Fill in details like:
- Username: andy or andy.mcmahon
- Display name: Andy McMahon
- Email address: your preferred email
- Password: choose “Send an email invitation” (AWS will send setup link)
3. Under Multi-factor authentication, tick Require MFA.
4. Leave groups blank for now (you can add later).
5. Click Add user.


### 3. Create Your Identity Center User

Once IAM Identity Center is enabled:
1. Go to Users → Add user
2. Fill in details:
- Username: andy or andy.mcmahon
- Display name: Andy McMahon
- Email address: your preferred email
- Password: choose “Send an email invitation” (AWS will send setup link)
3. Skip “register MFA” for now (you’ll enforce it globally later).
4.	Click Add user.
5.	Accept the invite from your email, set your password, and register your MFA device when prompted.

✅ You now have your first secure SSO identity.

### 4. Enforce MFA Globally (Optional but Recommended)
1. Go to Settings → Authentication in IAM Identity Center.
2. Under Multi-factor authentication (MFA), choose:
- Require MFA for all users ✅
- Authenticator app (TOTP) for MFA type
3. Save changes.

### 5. Verify Identity Center Region and Portal URL

Make sure you’re using the correct region (e.g., eu-west-2 for London).
Your login URL should look like:

`https://<your-org>.awsapps.com/start?region=eu-west-2`

Bookmark this — it’s your permanent login page.

### 6. Create and Attach a Permission Set

Now we’ll give your new Identity Center user admin-level permissions (through a permission set).
1. Go to IAM Identity Center → Permission sets → Create permission set
2. Choose:
- Predefined permission set
- Select AdministratorAccess
- Keep the defaults (1-hour session is fine for now)
3. Click Next → Submit

✅ This defines the “AdministratorAccess” bundle.

⸻

### 7. Assign Your User to Your AWS Account
1.	Go to IAM Identity Center → AWS accounts
2.	You’ll see your AWS account listed (usually just one)
3.	Select it → click Assign users or groups
4.	Choose your user (e.g. Andy McMahon)
5.	Pick the permission set you just made (AdministratorAccess)
6.	Click Submit

✅ That connects your identity → your account → the admin rights.

⸻

### 8. Log in via Your SSO Portal

Now you can stop using root forever.
1. Visit your SSO start URL, e.g. `https://<your-org>.awsapps.com/start`
2. Login as your new user identity.


---

