# Requirements

- R1 [auth]: No route outside the declared public routes is reachable without signing in.
- R2 [auth]: Routes that carry a declared role guard are reachable only by that role.
- R3 [auth]: The signed-in identity is set only after second-factor verification.
- R4 [auth]: Signing out always returns to the signed-out state.
