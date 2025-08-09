"use server";

export async function login(prevState, formData) {
  const email = formData.get("email");
  const password = formData.get("password");

  // Validate inputs (example)
  if (!email) return { errors: { email: "Email is required" } };
  if (!password) return { errors: { password: "Password is required" } };

  // Authenticate user (e.g., check against a database)
  const user = await db.user.findFirst({ where: { email } });
  if (!user) return { errors: { email: "Invalid email or password" } };

  // Verify password (example using bcrypt)
  const isValid = await bcrypt.compare(password, user.password);
  if (!isValid) return { errors: { password: "Invalid email or password" } };

  // Log the user in (e.g., set session cookies)
  await signIn(user);

  // Redirect on success
  return { success: true, redirectTo: "/dashboard" };
}