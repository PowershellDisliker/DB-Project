/* 
The Viewmodel will contain the state object definition and all API logic that is used on
this page. This format will be followed on all pages.
*/

export type loginViewModel = {
    username: string | null;
    password: string | null;

    failedLoginAttempt: boolean;
};