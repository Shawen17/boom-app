import {
  Label,
  Title,
  Outline,
  Button,
  Select,
  MiniContainer,
  Box,
  SignupContainer,
  SearchContainer,
  Input,
  SignupDisplay,
  PasswordWrapper,
  Password,
} from "../components/Styled";
import { useState, useEffect } from "react";
import { provinces } from "../components/utility/AdminAction";
import { Link, useNavigate } from "react-router-dom";
import { Form } from "reactstrap";
import { motion } from "framer-motion";
import CheckCircleOutlineIcon from "@mui/icons-material/CheckCircleOutline";

const Signup = () => {
  document.title = "Signup";
  const navigate = useNavigate();
  const [inputs, setInputs] = useState({});
  const [error, setError] = useState("");
  const [isValid, setIsValid] = useState(false);
  const [isMatch, setIsMatch] = useState(false);

  const handleChange = (event) => {
    setError("");
    const { name, value } = event.target;
    setInputs({ ...inputs, [name]: value });
  };

  const HandleSubmit = async (event) => {
    event.preventDefault();
    const email = inputs.email;
    const first_name = inputs.first_name;
    const last_name = inputs.last_name;
    const state = inputs.state;
    const password = inputs.password;
    const re_password = inputs.re_password;
    if (password === re_password) {
      navigate("/profile-form", {
        state: {
          email: email,
          state: state,
          first_name: first_name,
          last_name: last_name,
          password: password,
          re_password: re_password,
        },
      });
    } else {
      setError("password does not match");
    }
  };

  useEffect(() => {
    const validatePassword = (pwd) => {
      const pattern =
        /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,30}$/;

      if (inputs.re_password) {
        return pwd === inputs.password;
      } else {
        return pattern.test(pwd);
      }
    };
    if (inputs.re_password) {
      setIsMatch(validatePassword(inputs.re_password));
    } else {
      setIsValid(validatePassword(inputs.password));
    }
  }, [inputs]);

  return (
    <motion.div
      initial={{ scale: 0 }}
      animate={{ rotate: 0, scale: 1 }}
      transition={{
        type: "spring",
        stiffness: 260,
        damping: 20,
      }}
    >
      <SignupContainer>
        <Title style={{ marginTop: 20 }}>Add your Details</Title>

        <SignupDisplay>
          <Form style={{ width: "100%" }} onSubmit={HandleSubmit}>
            <MiniContainer>
              <Box>
                <Label>First Name</Label>
                <SearchContainer>
                  <Input
                    required
                    placeholder="First Name"
                    type="text"
                    name="first_name"
                    value={inputs.first_name || ""}
                    onChange={handleChange}
                  />
                </SearchContainer>
              </Box>
              <Box>
                <Label>Last Name</Label>
                <SearchContainer>
                  <Input
                    required
                    placeholder="Your Surname"
                    type="text"
                    name="last_name"
                    value={inputs.last_name || ""}
                    onChange={handleChange}
                  />
                </SearchContainer>
              </Box>
            </MiniContainer>
            <MiniContainer>
              <Box>
                <Label>Email</Label>
                <SearchContainer>
                  <Input
                    placeholder="Email Address"
                    type="email"
                    name="email"
                    value={inputs.email || ""}
                    required
                    onChange={handleChange}
                  />
                </SearchContainer>
              </Box>
              <Box>
                <Label htmlFor="state">Province</Label>
                <SearchContainer>
                  <Select
                    required
                    name="state"
                    value={inputs.state || ""}
                    onChange={handleChange}
                  >
                    {provinces.map((province) => (
                      <option key={province.id} value={province.name}>
                        {province.name}
                      </option>
                    ))}
                  </Select>
                </SearchContainer>
              </Box>
            </MiniContainer>
            <div style={{ fontSize: 13, color: "red" }}>{error}</div>
            <MiniContainer>
              <Box>
                <Label>Password</Label>
                <PasswordWrapper>
                  <Password
                    pattern="/^(?=.*[a-z])(?=.*[A-Z])(?=.*d)(?=.*[!@#$%^&*])[A-Za-zd!@#$%^&*]{8,30}$/"
                    type="password"
                    title="lower,upper,number, special character"
                    onChange={handleChange}
                    placeholder="Password"
                    name="password"
                    value={inputs.password || ""}
                    required
                  />
                  {isValid && (
                    <span className="checkmark">
                      <CheckCircleOutlineIcon style={{ fontSize: 15 }} />
                    </span>
                  )}
                </PasswordWrapper>
              </Box>

              <Box>
                <Label>Confirm Password</Label>
                <PasswordWrapper>
                  <Password
                    title="same with password"
                    pattern="/^(?=.*[a-z])(?=.*[A-Z])(?=.*d)(?=.*[!@#$%^&*])[A-Za-zd!@#$%^&*]{8,30}$/"
                    required
                    placeholder="Confirm Password"
                    type="password"
                    name="re_password"
                    value={inputs.re_password || ""}
                    onChange={handleChange}
                  />
                  {isMatch && (
                    <span className="checkmark">
                      <CheckCircleOutlineIcon style={{ fontSize: 15 }} />
                    </span>
                  )}
                </PasswordWrapper>
              </Box>
            </MiniContainer>
            <Button type="submit">Submit</Button>
          </Form>

          <Outline>
            <div style={{ marginRight: 4 }}>Already have an account?</div>
            <Link
              style={{ color: "#18a558" }}
              className="nav-link sidebar-link"
              to="/"
            >
              Login
            </Link>
          </Outline>
        </SignupDisplay>
      </SignupContainer>
    </motion.div>
  );
};

export default Signup;
