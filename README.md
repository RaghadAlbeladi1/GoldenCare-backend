<p align="center">
  <a href="https://generalassemb.ly/">
    <img src="https://github.com/user-attachments/assets/0284af1b-bf15-408c-b724-98868f976667" alt="General Assembly" height="80"/>
  </a>
  &nbsp;&nbsp;&nbsp;&nbsp;
  <a href="https://sda.edu.sa/">
  </a><img width="500" height="80" alt="Sda-logo-color" src="https://github.com/user-attachments/assets/5edb2838-4fe6-4b18-b80d-706b31f56a64" />

</p>


##  Authentication

| HTTP Method | Path | Action | Description |
|------------|------|--------|-------------|
| `POST` | `/auth/register` | create | Register a new user (patient) |
| `POST` | `/auth/login` | create | User login (returns token) |
| `POST` | `/auth/logout` | destroy | User logout |

## Users (Patients)

| HTTP Method | Path | Action | Description |
|------------|------|--------|-------------|
| `GET` | `/users/profile` | show | Get current user profile |
| `PUT` | `/users/profile` | update | Update user profile |
| `PATCH` | `/users/profile` | update | Partially update user profile |
| `DELETE` | `/users/profile` | destroy | Delete user account |


##  Caregivers

| HTTP Method | Path | Action | Description |
|------------|------|--------|-------------|
| `GET` | `/caregivers` | index | List all caregivers |
| `GET` | `/caregivers/:id` | show | Show caregiver details (including service) |


## Services

| HTTP Method | Path | Action | Description |
|------------|------|--------|-------------|
| `GET` | `/services` | index | List all active services |
| `GET` | `/services/:id` | show | Show service details (including caregiver info) |
| `GET` | `/services/search` | index | Search services by name or specialization |


## Appointments

| HTTP Method | Path | Action | Description |
|------------|------|--------|-------------|
| `GET` | `/appointments` | index | List all appointments for current user |
| `POST` | `/appointments` | create | Book a new appointment (cancels any pending appointment) |
| `GET` | `/appointments/:id` | show | Show appointment details |
| `PUT` | `/appointments/:id` | update | Update appointment (reschedule or add notes) |
| `PATCH` | `/appointments/:id` | update | Partially update appointment |
| `DELETE` | `/appointments/:id` | destroy | Cancel appointment |
| `PUT` | `/appointments/:id/complete` | update | Mark appointment as completed |
| `GET` | `/appointments/current` | show | Get current active appointment |
| `GET` | `/appointments/history` | index | Get all completed appointments |

##  EHR (Electronic Health Records)

| HTTP Method | Path | Action | Description |
|------------|------|--------|-------------|
| `GET` | `/ehr` | index | Get all EHR records for current user |
| `POST` | `/ehr/notes` | create | Add a new note |
| `POST` | `/ehr/medications` | create | Add medication information |
| `GET` | `/ehr/:id` | show | Show specific EHR record |
| `PUT` | `/ehr/:id` | update | Update EHR record |
| `PATCH` | `/ehr/:id` | update | Partially update EHR record |
| `DELETE` | `/ehr/:id` | destroy | Delete EHR record |
| `GET` | `/ehr/notes` | index | Get all notes only |
| `GET` | `/ehr/medications` | index | Get all medications only |

## Reviews 

| HTTP Method | Path | Action | Description |
|------------|------|--------|-------------|
| `GET` | `/reviews` | index | Get all public reviews (displayed on website) |
| `POST` | `/reviews` | create | Add review (requires completed service) |
| `GET` | `/reviews/:id` | show | Show review details |
| `GET` | `/users/reviews` | index | Get all reviews by current user |
| `DELETE` | `/reviews/:id` | destroy | Delete own review |

